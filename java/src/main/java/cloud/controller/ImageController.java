package cloud.controller;

import cloud.model.course.Course;
import cloud.model.course.CourseService;
import cloud.model.course.task.Task;
import cloud.model.course.task.TaskService;
import cloud.model.course.task.question.submission.image.ImageService;
import cloud.model.user.User;
import cloud.model.user.UserService;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.view.RedirectView;

import javax.annotation.Resource;
import java.io.IOException;
import java.util.Date;


@RestController
public class ImageController extends BaseController {

    @Resource
    private ImageService imageService;

    @Resource
    private UserService userService;

    @Resource
    private CourseService courseService;

    @Resource
    private TaskService taskService;

    @GetMapping(value = { "/image/{imageId}" })
    public RedirectView showImage(@PathVariable String imageId) {

        RedirectView redirectView = imageService.imageIdToRedirect(imageId);

        return redirectView;

    }

    @GetMapping(value = { "/test" })
    public Result test() {
        Course course = new Course();
        User user =  new User();
        courseService.save(course);
        userService.save(user);

        Task task = new Task(course, "sd", "ss", new Date(), new Date());
        taskService.save(task);
        HttpGet httpGet = new HttpGet("http://www.clavier.moe:8088");
        CloseableHttpClient httpclient = HttpClients.createDefault();
        CloseableHttpResponse response = null;
        try {
            response = httpclient.execute(httpGet);
            return new Result("sd", "ss", response);
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            //4.处理结果
        } finally {
            try {
                response.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }


        return new Result("sd", "ss", httpGet);

    }

}

