package cloud.model.course.task.question.marking.annotation;

import lombok.Data;

import javax.persistence.*;

@Entity
@Table(name = "Annotation")
@Data
public class Annotation {

    @Id
    @GeneratedValue
    private Long id;

    // check, cross, comment
    private String type;

    private int page_num;

    private Double x;

    private Double y;

    public Annotation() {}

    public Annotation(String _type, int _page_num, Double _x, Double _y) {
        type = _type;
        page_num = _page_num;
        x = _x;
        y = _y;
    }


}
