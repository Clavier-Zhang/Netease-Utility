//package cloud.common;
//import cloud.model.user.User;
//import cloud.model.user.UserRepository;
//import cloud.model.user.UserService;
//import cloud.model.user.instructor.InstructorService;
//import cloud.model.user.student.StudentService;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.web.bind.annotation.GetMapping;
//import org.springframework.web.bind.annotation.PostMapping;
//import org.springframework.web.bind.annotation.RequestParam;
//import org.springframework.web.bind.annotation.RestController;
//
//import javax.annotation.Resource;
//import javax.servlet.http.HttpServletRequest;
//
//@RestController
//public class SecurityController extends BaseController {
//
//    @Autowired
//    private UserRepository userRepository;
//
//
//    @PostMapping("/security/signIn")
//    public Result login(HttpServletRequest request) {
//
//        String email = request.getParameter("email");
//        String password = request.getParameter("password");
//
////        User user = userRepository.findByEmail(email);
////
////        if (user == null) {
////            return new Result("fail", "email not exist");
////        }
////
////        if (!user.getPassword().equals(password)) {
////            return new Result("fail", "wrong password");
////        }
//        return new Result("success", "sign in");
//
//    }
//
//    @PostMapping("/security/signup")
//    public Result signup(HttpServletRequest request) {
//
//        String email = request.getParameter("email");
//        String password = request.getParameter("password");
//
//
//        return new Result("success", "good");
//    }
//
//    @GetMapping("/user/logout")
//    public String Logout(@RequestParam(value="name", defaultValue="World") String name) {
//
//        return "111111111";
//    }
//}
