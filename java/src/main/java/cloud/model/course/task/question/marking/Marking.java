package cloud.model.course.task.question.marking;

import cloud.model.course.task.question.Question;
import cloud.model.course.task.question.marking.annotation.Annotation;
//import cloud.model.user.instructor.Instructor;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "Marking")
@Data
public class Marking {

    @Id
    @GeneratedValue
    private Long id;

    private String marker;

    private Double mark_obtained;

    private Date date = new Date();

    @OneToOne
    @JsonIgnore
    private Question question;

    @OneToMany
    private List<Annotation> annotations = new ArrayList<>();

    public Marking() {};

    public Marking(Question _question, String _marker, Double _mark_obtained) {
        marker = _marker;
        mark_obtained = _mark_obtained;
        question = _question;
        question.getMarkings().add(this);
    }


}
