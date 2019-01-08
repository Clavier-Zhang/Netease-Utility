package cloud.model.user;

import javax.persistence.*;

import lombok.Data;


@Entity
@Table(name = "user")
@Data
public class User {

    @Id
    @GeneratedValue
    private Long id;

    @Column(unique=true)
    private Long uid;

    private String nickname;

    private int gender;

    private Boolean searched = false;

    private Boolean visible = true;

    public User() {}

}