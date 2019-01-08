package cloud.model.course.task.question.submission.image;


import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;

@Entity
@Table(name = "image")
@Data
public class Image {

    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator( name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    private String id;

    private String format;

    public Image() {};

    public Image(String _format) {
        format = _format;
    }

    @JsonIgnore
    public String getName() {
        return id + "." + format;
    }

}
