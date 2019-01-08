package cloud.model.course.task.question;

import cloud.model.course.task.question.marking.Marking;
import cloud.model.course.task.question.marking.MarkingService;
import cloud.model.course.task.question.submission.Submission;
import cloud.model.course.task.question.submission.SubmissionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;

@Transactional
@Service
public class QuestionService {

    @Autowired
    private QuestionRepository questionRepository;

    @Resource
    private MarkingService markingService;

    @Resource
    private SubmissionService submissionService;

    public void save(Question question) {
        questionRepository.save(question);
    }

    public void delete(Question question) {
        for (Marking marking : question.getMarkings()) {
            markingService.delete(marking);
        }
        for (Submission submission : question.getSubmissions()) {
            submissionService.delete(submission);
        }
        questionRepository.delete(question);
    }

    public void deleteAll() {
        Iterable<Question> questions = questionRepository.findAll();
        for (Question question : questions) {
            delete(question);
        }
    }

}
