window.data = {
    test:function(index){
        var result = {};
        $.ajax({
                    url:"tmp?id="+index,
                    type:"get",
                    async:false,
                    dataType:"json",
                    success:function(data){
                        result = data;
                    }
                });
        return result;
    },
    test1:function(name,sex){
        var result = {};
        $.ajax({
                    url:"tmp?id="+index,
                    type:"get",
                    async:false,
                    dataType:"json",
                    data:{
                        name:name,
                        sex:sex
                    },
                    success:function(data){
                        console.log(data);
                    }
                });
    },
    salePredict:function(saleType,saleKey,saleYear,saleMonth,saleModel,useCarInfo,useRateInfo,useFutureInfo,useTireInfo,useNormalization,useShipmentInfo){
        var result = {};
        var tmp = "";
        if(saleType == "1"){
            tmp = "&type=1&customerId="+saleKey;
        }
        else if(saleType == "2"){
            tmp = "&type=2&materialGroup="+saleKey;
        }
        else if(saleType == '3'){
            tmp = "&type=3&typeBrand="+saleKey;
        }else{
             return result;
        }
        $.ajax({
            url:"sale/predict?year="+saleYear+"&month="+saleMonth+tmp+"&saleModel="+saleModel+"&useCarInfo="+useCarInfo+"&useRateInfo="+useRateInfo+"&useFutureInfo="+useFutureInfo+"&useTireInfo="+useTireInfo+"&useNormalization="+useNormalization+"&useShipmentInfo="+useShipmentInfo,
            type:"get",
            async:false,
            dataType:"json",
            success:function(data){
                result = data;
            }
        });
        return result;
    },

    dataTire:function(year,month){
        var result = {};
        $.ajax({
            url:"data/tire?year="+year+"&month="+month,
            type:"get",
            async:false,
            dataType:"json",
            success:function(data){
                result = data;
            }
        });
        return result;
    },

    dateTireBrand:function(cate){
        var result = {};
        $.ajax({
            url:"data/tirebrand?cate="+cate,
            type:"get",
            async:false,
            dataType:"json",
            success:function(data){
                result = data;
            }
        });
        return result;
    },
    dateTireGroup:function(cate){
        var result = {};
        $.ajax({
            url:"data/tiregroup?cate="+cate,
            type:"get",
            async:false,
            dataType:"json",
            success:function(data){
                result = data;
            }
        });
        return result;
    },
    dateCustomerInfo:function(cate){
        var result = {};
        $.ajax({
            url:"data/customerinfo?cate="+cate,
            type:"get",
            async:false,
            dataType:"json",
            success:function(data){
                result = data;
            }
        });
        return result;
    },
    upload:function(file,newName,comment){
        var formData = new FormData();
        formData.append('file', file);
        formData.append('newName', newName);
        formData.append('comment', comment);
        $.ajax({
             url:"file/upload",
             type: 'POST',
             data: formData,
             processData: false,
             contentType: false,
             error:function () {
                 alert('上传失败');
             },
             success:function (msg) {
                 alert("上传成功");
                 location.reload();
             }
         });
    }

}

//salePredict:function(type,key,year,month){
//        var result = {};
//        var tmp = "";
//        if(type == "1"){
//            tmp = "&type=1&customerId="+key;
//        }
//        else if(type == "2"){
//            tmp = "&type=2&materialGroup="+key;
//        }
//        else if(type == '3'){
//            tmp = "&type=3&typeBrand="+key;
//        }
//        else{
//            return result;
//        }
//
//        $.ajax({
//            url:"sale/predict?year="+year+"&month="+month+tmp
//            type:"get",
//            async:false,
//            dataType:"json",
//            success:function(data){
//                result = data;
//            }
//        });
//        return result;
//    }