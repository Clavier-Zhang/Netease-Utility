package cloud.model.user;

import javax.persistence.*;

import cloud.model.user.role.Role;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;


@Entity
@Table(name = "user")
@Data
public class User {

    @Id
    @GeneratedValue
    private Long id;

    private String email;

    @JsonIgnore
    private String password;

    private String name;

    @OneToMany
    List<Role> roles = new ArrayList();

    public User(String _email, String _password, String _name) {
        email = _email;
        password = _password;
        name = _name;
    }

    public User() {}

}