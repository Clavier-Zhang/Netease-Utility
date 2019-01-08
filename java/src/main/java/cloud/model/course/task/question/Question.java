package cloud.model.course.task.question;


import cloud.model.course.task.Task;
import cloud.model.course.task.question.marking.Marking;
import cloud.model.course.task.question.submission.Submission;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "Question")
@Data
public class Question {

    @Id
    @GeneratedValue
    private Long id;

    private int question_num;

    private int total_mark;

    private boolean is_submitted = false;

    private boolean is_marked = false;

    @OneToOne
    @JsonIgnore
    private Task task;

    @OneToMany
    private List<Marking> markings = new ArrayList();

    @OneToMany
    private List<Submission> submissions = new ArrayList();

    public Question() {};

    public Question(Task _task, int _question_num, int _total_mark) {
        task = _task;
        question_num = _question_num;
        total_mark = _total_mark;
        task.getQuestions().add(this);
    }

}
