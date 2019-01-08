package cloud.model.course.task.question.submission.image;


import cloud.controller.BaseController;
import com.aliyun.oss.OSSClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.view.RedirectView;

import java.io.*;
import java.util.Optional;

@Transactional
@Service
public class ImageService extends BaseController {

    @Autowired
    private ImageRepository imageRepository;

    public Iterable<Image> findAll() {
        return imageRepository.findAll();
    }


    // for aliyun
    private String endpoint = "http://oss-us-west-1.aliyuncs.com";
    private String accessKeyId = "LTAILFyLtkB3kAKk";
    private String accessKeySecret = "icfVv3qypFczNjWnQYX0kVqiyAb4Zl";
    private String bucketName = "mushroom-server";

    public void delete(Image image) {
        try {
            String objectName = image.getName();
            OSSClient ossClient = new OSSClient(endpoint, accessKeyId, accessKeySecret);
            ossClient.deleteObject(bucketName, objectName);
            ossClient.shutdown();
            imageRepository.delete(image);
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    public void deleteAll() {
        Iterable<Image> images = imageRepository.findAll();
        for (Image image : images) {
            delete(image);
        }
    }


    public Image createImage(MultipartFile file) {
        try {

            String suffix = file.getOriginalFilename().substring(file.getOriginalFilename().lastIndexOf("."));
            String format = file.getOriginalFilename().substring(file.getOriginalFilename().lastIndexOf(".")+1);
            Image image = new Image(format);
            imageRepository.save(image);
            String fileName = image.getId() + suffix;
            OSSClient ossClient = new OSSClient(endpoint, accessKeyId, accessKeySecret);
            ossClient.putObject(bucketName, fileName, new ByteArrayInputStream(file.getBytes()));
            ossClient.shutdown();
            imageRepository.save(image);
            return image;
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return null;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }




    public RedirectView imageIdToRedirect(String imageId) {

        System.out.println(imageId);

        Optional<Image> image = imageRepository.findById(imageId);

        String name = image.get().getName();

        RedirectView redirectView = new RedirectView();

        redirectView.setUrl(imagePath + name);

        return redirectView;

    }

}
