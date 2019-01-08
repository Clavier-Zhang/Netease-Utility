package cloud.model.user.role;

import cloud.model.course.Course;
import cloud.model.user.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Transactional
@Service
public class RoleService {

    @Autowired
    private RoleRepository roleRepository;

    public void save(Role role) {
        roleRepository.save(role);
    }

    public void delete(Role role) {
        role.getCourse().getMembers().remove(role);
        role.getUser().getRoles().remove(role);
        roleRepository.delete(role);
    }

    public void deleteAll() {
        Iterable<Role> roles = roleRepository.findAll();
        for (Role role : roles) {
            delete(role);
        }
    }

    public void addRole(Role self, User other, Course course, String type) {
        if (!self.getType().equals("instructor")) {
            return;
        }
        Role role = new Role(other, course, type);
        save(role);
    }

    public void removeRole(Role self, Role other, Course course) {
        if (!self.getType().equals("instructor")) {
            return;
        }
        delete(other);
    }

}
