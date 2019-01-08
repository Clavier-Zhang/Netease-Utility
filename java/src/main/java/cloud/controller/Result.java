package cloud.controller;

import lombok.Data;

@Data
public class Result {


    public Result(int code) {
        this.code = code;
    }

    public Result(int code, String description) {
        this.code = code;
        this.description = description;
    }

    public Result(int code, String description, Object obj) {
        this.code = code;
        this.description = description;
        this.detail = obj;
    }

    int code;

    String description;

    Object detail;


}
