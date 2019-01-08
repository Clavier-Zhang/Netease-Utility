package cloud.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;


@RequestMapping(("/api"))
public class BaseController {

    public String currentPath = "/home/backend/upload/";

    public String imagePath = "https://mushroom-server.oss-us-west-1.aliyuncs.com/";

    public Date stringToDate(String paramDate) throws ParseException {
        String realDate = paramDate.substring(1, 20) + ".000+0000";
        DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSZ");
        Date date = sdf.parse(realDate);
        return date;
    }

    public boolean isEmpty(String word) {
        return word == null || word.equals("");
    }


}
