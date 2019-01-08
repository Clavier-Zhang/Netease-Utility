package cloud.model.user;


import cloud.controller.BaseController;
import cloud.controller.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.Arrays;
import java.util.List;

@RestController
public class UserController extends BaseController {

    @Autowired
    private UserRepository userRepository;

    private Boolean unsearch_trigger = true;

    @PostMapping("/user/all")
    public Result all() {

        Iterable<User> users = userRepository.findAll();

        return new Result(200, "all users", users);

    }

    @PostMapping("/user/deleteAll")
    public Result deleteAll() {

        userRepository.deleteAll();

        return new Result(200, "delete all users");

    }

    @PostMapping("/user/save_one")
    public Result save_one(@ModelAttribute User user) {
        try {
            userRepository.save(user);

        } catch (Exception e) {
            System.out.println(e);
        }
        System.out.println("success");
        return new Result(200, "sd", user);
    }

    @PostMapping("/user/save_all")
    public Result save_one(@RequestBody User[] users) {
        int success = 0;
        int fail = 0;
        for (User user : users) {
            try {
                userRepository.save(user);
                success++;
            } catch (Exception e) {
                System.out.println(e);
                fail++;
            }
        }
        return new Result(200, "sd", users);
    }

    @PostMapping("/user/get_range_id_users")
    public Result get_range_id_users(HttpServletRequest request) {

        Long start = Long.parseLong(request.getParameter("start"));
        Long end = Long.parseLong(request.getParameter("end"));
        String is_gril_string = request.getParameter("end");

        if (is_gril_string == null || is_gril_string.equals("") || !Boolean.parseBoolean(is_gril_string)) {
            Iterable<User> users = userRepository.findAllByIdGreaterThanEqualAndIdLessThanEqual(start, end);
            return new Result(200, "return range users", users);
        }

        Iterable<User> users = userRepository.findAllByIdGreaterThanEqualAndIdLessThanEqualAndGender(start, end, 2);
        return new Result(200, "return range users (girls only)", users);
    }

    @PostMapping("/user/get_unsearched_users")
    public Result get_unsearched_users(HttpServletRequest request) {
        this.unsearch_trigger = !this.unsearch_trigger;

        if (this.unsearch_trigger) {
            List<User> users = userRepository.findTop100BySearchedFalseOrderByIdAsc();
            return new Result(200, "return unsearched users", this.unsearch_trigger);
        }

        List<User> users = userRepository.findTop100BySearchedFalseOrderByIdDesc();
        return new Result(200, "return unsearched users", this.unsearch_trigger);
    }


}
