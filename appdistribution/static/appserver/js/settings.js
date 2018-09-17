 $(document).ready(function(){
     $("#uploadFileFormiOS").validate({
               rules: {
                   product: {
                     required: true
                   },
                   bundleid: {
                    required: true
                   },
                   displayimage: {
                    required: true,
                    url: true
                   },
                   fullsizeimage: {
                    required: true,
                    url: true
                   }
               },
         messages:{
             bundleid: {
                     required: "Please enter bundle id!"
                   },
             product: {
                required: "Please enter product name!"
             },
             displayimage: {
                required: "Please enter display image!"
             },
             fullsizeimage: {
                required: "Please enter full size image!"
             }

         }
    });

    $("#addAndroidProduct").validate({
               rules: {
                   product: {
                    required: true
                   }
               },
         messages:{
             uploadfile: {
                     required: "Please enter product name!"
                   }
         }
    });
});