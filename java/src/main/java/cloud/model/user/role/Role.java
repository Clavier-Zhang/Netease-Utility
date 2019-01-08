package cloud.model.user.role;


import cloud.model.course.Course;
import cloud.model.user.User;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.persistence.*;

@Entity
@Table(name = "role")
@Data
public class Role {

    @Id
    @GeneratedValue
    private Long id;

    private String type;

    @OneToOne
    @JsonIgnore
    private Course course;

    @OneToOne
    @JsonIgnore
    private User user;

    public Role() {};

    public Role(User _user, Course _course, String type) {
        user = _user;
        course = _course;
        _user.getRoles().add(this);
        course.getMembers().add(this);
    }

}
