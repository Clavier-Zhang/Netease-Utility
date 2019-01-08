package cloud.model.course.task.question.marking;

import cloud.model.course.task.question.marking.annotation.Annotation;
import cloud.model.course.task.question.marking.annotation.AnnotationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.List;

@Transactional
@Service
public class MarkingService {

    @Autowired
    private MarkingRepository markingRepository;

    @Resource
    private AnnotationService annotationService;

    public void save(Marking marking) {
        markingRepository.save(marking);
    }

    public void delete(Marking marking) {
        // delete annotations fields
        List<Annotation> annotations = marking.getAnnotations();
        for (Annotation annotation : annotations) {
            annotationService.delete(annotation);
        }
        markingRepository.delete(marking);
    }

    public void deleteAll() {
        Iterable<Marking> markings = markingRepository.findAll();
        for (Marking marking : markings) {
            delete(marking);
        }
    }

}
