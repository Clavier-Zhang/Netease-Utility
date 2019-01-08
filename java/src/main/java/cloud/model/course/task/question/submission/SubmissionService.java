package cloud.model.course.task.question.submission;


import cloud.model.course.task.question.submission.image.Image;
import cloud.model.course.task.question.submission.image.ImageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;

@Transactional
@Service
public class SubmissionService {

    @Autowired
    private SubmissionRepository submissionRepository;

    @Resource
    private ImageService imageService;

    public void delete(Submission submission) {
        for (Image image : submission.getImages()) {
            imageService.delete(image);
        }
        submissionRepository.delete(submission);
    }

    public void deleteAll() {
        Iterable<Submission> submissions = submissionRepository.findAll();
        for (Submission submission : submissions) {
            delete(submission);
        }
    }

    public void save(Submission submission) {
        submissionRepository.save(submission);
    }



}
