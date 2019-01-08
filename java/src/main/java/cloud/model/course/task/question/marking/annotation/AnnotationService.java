package cloud.model.course.task.question.marking.annotation;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Transactional
@Service
public class AnnotationService {

    @Autowired
    private AnnotationRepository annotationRepository;

    public void save(Annotation annotation) {
        annotationRepository.save(annotation);
    }

    public void delete(Annotation annotation) {
        annotationRepository.delete(annotation);
    }

    public void deleteAll() {
        annotationRepository.deleteAll();
    }


}
