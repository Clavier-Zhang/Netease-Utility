package cloud.model.course.task.question.submission;

import cloud.model.course.task.question.Question;
import cloud.model.course.task.question.submission.image.Image;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "Submission")
@Data
public class Submission {

    @Id
    @GeneratedValue
    private Long id;

    @OneToMany
    private List<Image> images = new ArrayList<>();

    @OneToOne
    @JsonIgnore
    private Question question;

    public Submission() {};

    public Submission(Question _question) {};

}
