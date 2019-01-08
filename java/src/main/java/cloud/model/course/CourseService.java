package cloud.model.course;


import cloud.model.course.task.Task;
import cloud.model.course.task.TaskService;
import cloud.model.user.role.Role;
import cloud.model.user.role.RoleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;


@Transactional
@Service
public class CourseService {

    @Autowired
    private CourseRepository courseRepository;

    @Resource
    private TaskService taskService;

    @Resource
    private RoleService roleService;

    public void save(Course course) {
        courseRepository.save(course);
    }

    public void delete(Course course) {
        for (Task task : course.getTasks()) {
            taskService.delete(task);
        }
        for (Role member : course.getMembers()) {
            roleService.delete(member);
        }
        courseRepository.delete(course);
    }

    public void deleteAll() {
        Iterable<Course> courses = courseRepository.findAll();
        for (Course course : courses) {
            delete(course);
        }
    }

}
