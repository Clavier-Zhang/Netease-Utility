package cloud.model.course.task;


import cloud.model.course.Course;
import cloud.model.course.task.question.Question;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "Task")
@Data
public class Task {

    @Id
    @GeneratedValue
    private Long id;

    private String name;

    // midterm or tasks
    private String type;

    private Boolean score_visible = false;

    private Date submission_due_day;

    private Date marking_due_day;

    @OneToOne
    @JsonIgnore
    private Course course;

    @OneToMany
    private List<Question> questions = new ArrayList<>();

    public Task() {};

    public Task(Course _course,  String _name, String _type, Date _submission_due_day, Date _marking_due_day) {
        course = _course;
        name = _name;
        type = _type;
        submission_due_day = _submission_due_day;
        marking_due_day = _marking_due_day;
        course.getTasks().add(this);
    }

}
