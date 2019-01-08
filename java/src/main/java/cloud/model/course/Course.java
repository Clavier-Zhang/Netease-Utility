package cloud.model.course;


import cloud.model.course.task.Task;
//import cloud.model.user.instructor.Instructor;
//import com.fasterxml.jackson.annotation.JsonIgnore;
import cloud.model.user.role.Role;
import lombok.Data;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "Course")
@Data
public class Course {

    @Id
    @GeneratedValue
    private Long id;

    private String name;

    private String term;

    @OneToMany
    private List<Task> tasks = new ArrayList();

    @OneToMany
    private List<Role> members = new ArrayList();

    public Course() {};

    public Course(String _name, String _term) {
        name = _name;
        term = _term;
    }

}
