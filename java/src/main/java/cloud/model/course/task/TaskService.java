package cloud.model.course.task;

import cloud.model.course.task.question.Question;
import cloud.model.course.task.question.QuestionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;

@Transactional
@Service
public class TaskService {

    @Autowired
    private TaskRepository taskRepository;

    @Resource
    private QuestionService questionService;

    public void delete(Task task) {
        for (Question question : task.getQuestions()) {
            questionService.delete(question);
        }
        taskRepository.delete(task);
    }

    public void deleteAll() {
        Iterable<Task> tasks = taskRepository.findAll();
        for (Task task : tasks) {
            delete(task);
        }
    }

    public void save(Task task) {
        taskRepository.save(task);
    }

}
