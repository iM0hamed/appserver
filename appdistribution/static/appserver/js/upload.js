 $(document).ready(function(){
     $("#uploadFileFormiOS").validate({
               rules: {
                   bundleid: {
                     required: true
                   } ,

                   uploadfile: {
                    required: true
                   }
               },
         messages:{
             bundleid: {
                     required: "the bundleid is required"
                   },
             uploadfile: {
                required: "Please select an ipa file"
             }
         }
    });

    $("#uploadFileFormAndroid").validate({
               rules: {
                   uploadfile: {
                    required: true
                   }
               },
         messages:{
             uploadfile: {
                     required: "Please select a apk file"
                   }
         }
    });
});