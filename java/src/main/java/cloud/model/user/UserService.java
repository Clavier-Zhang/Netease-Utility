package cloud.model.user;

import cloud.model.course.Course;
import cloud.model.course.CourseService;
import cloud.model.user.role.Role;
import cloud.model.user.role.RoleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;


@Transactional
@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Resource
    private RoleService roleService;

    @Resource
    private CourseService courseService;

    public void save(User user) {
        userRepository.save(user);
    }

    public void delete(User user) {
        for (Role role : user.getRoles()) {
            roleService.delete(role);
        }
        userRepository.delete(user);
    }

    public void deleteAll() {
        userRepository.deleteAll();
    }

    public void createCourse(User user, String courseName, String courseTerm) {
        Course course = new Course(courseName, courseTerm);
        courseService.save(course);
        Role role = new Role(user, course, "instructor");
        roleService.save(role);
    }

}
