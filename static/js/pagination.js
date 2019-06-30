$.fn.pagination = function pagination(fn){
    if($(this).attr('data-to-page') == 'False'){
        return false;
    }
    if(!fn||typeof fn!="function"){
        return false;
    }
    let pageIndex= Number($(this).attr('data-page-no'))||1;
    pageSize=30,
    count= Number($(this).attr('data-count'))||0,
    container= this,
    callback=fn||function(){};
    let pageCount =Math.ceil(count/pageSize);
    if(pageCount==0){
         return false ;
    }
    if(pageCount<pageIndex){
         return false;
    }
    /*事件绑定*/
    function bindEvent(){
        //首页
        $(container).find('.pg-first').unbind("click").bind("click",function(){
            callback(1);
        })
        //尾页
        $(container).find('.pg-last').unbind("click").bind("click",function(){
            callback(pageCount);
        })
        //上一页事件
        $(container).find(".pg-prev").unbind("click").bind("click",function(){
            if(pageIndex <=1){
                return false ;
            }
            if(typeof callback=="function"){
                pageIndex--;
                pageIndex = pageIndex<1?1:pageIndex;
                callback(pageIndex);
            }
        });
        //下一页事件
        $(container).find(".pg-next").unbind("click").bind("click",function(){
            if(pageIndex ==pageCount){
                return false ;
            }
            if(typeof callback=="function"){
                pageIndex++;
                pageIndex =pageIndex >pageCount?pageCount:pageIndex;
                callback(pageIndex);
            }
        });
        //具体页码事件
        $(container).find("a:not(.pg-more):not(.pg-prev):not(.pg-next):not(.pg-first):not(.pg-last):not(.pg-jump)")
            .unbind("click").bind("click",function(){
            pageIndex = $(this).html();
            pageIndex = isNaN(pageIndex)?1:pageIndex;
            if(typeof callback=="function"){
                callback(pageIndex);
            }
        });
        $(container).find(".pg-jump").unbind("click").bind("click",function(){
            pageIndex = $(container).find('input').val();
            pageIndex = (isNaN(pageIndex)|| pageIndex<=0)?1:pageIndex;
            pageIndex = pageIndex >pageCount?pageCount:pageIndex;
            if(typeof callback=="function"){
                callback(pageIndex);
            }
        });
    };
    /*画样式*/
    function printHead(){
        let html=[];
        html.push('<a class="pg-first fed-btns-info fed-rims-info fed-hide fed-show-xs-inline '+(pageIndex==1?"fed-btns-disad":"")+'">首页</a>')
        html.push('<a class="pg-prev fed-btns-info fed-rims-info fed-show-xs-inline '+(pageIndex==1?"fed-btns-disad":"")+'">上页</a>');
        return html.join("");
    }
    function printBody(){
        let html=[];
        let render=function(num,start){
            start=start||1;
            for(let i=start;i<=num;i++){
                html.push('<a class="fed-btns-info fed-rims-info fed-hide fed-show-sm-inline '+(pageIndex==i?"fed-btns-green":"")+'">'+i+'</a>');
            }
        }
        if(pageCount<=5){
             render(pageCount);
        }else{
             if(pageIndex <4){
                 render(4);
                 html.push('<a class="pg-more fed-btns-info fed-rims-info fed-hide fed-show-sm-inline fed-btns-disad" href="javascript:;">...</a>');
                 html.push('<a class="fed-btns-info fed-rims-info fed-hide fed-show-sm-inline">'+pageCount+'</a>');
             }else{
                 html.push('<a class="fed-btns-info fed-rims-info fed-hide fed-show-sm-inline">'+1+'</a>');
                 html.push('<a class="pg-more fed-btns-info fed-rims-info fed-hide fed-show-sm-inline fed-btns-disad" href="javascript:;">...</a>');
                 if(pageCount-pageIndex>3){
                         render(pageIndex+1,pageIndex-1);
                         html.push('<a class="pg-more fed-btns-info fed-rims-info fed-hide fed-show-sm-inline fed-btns-disad" href="javascript:;">...</a>');
                         html.push('<a class="fed-btns-info fed-rims-info fed-hide fed-show-sm-inline">'+pageCount+'</a>');
                  }else{
                         render(pageCount,pageCount-3);
                  }
             }
        }
        return html.join("");
    }
    function printTail(){
        let html=[];
        html.push('<a class="fed-btns-info fed-rims-info fed-hide fed-show-xs-inline" href="javascript:;">'+pageIndex+'/'+pageCount+'</a>')
        html.push('<a class="pg-next fed-btns-info fed-rims-info'+(pageIndex==pageCount?" fed-btns-disad":"")+'">下页</a>');
        html.push('<a class="pg-last fed-btns-info fed-rims-info fed-hide fed-show-xs-inline">尾页</a>');
        html.push('<input class="fed-rims-info" type="text" placeholder="输入页码" autocomplete="off">');
        html.push('<a class="pg-jump fed-btns-info fed-rims-info fed-page-jump">跳转</a>');
        return html.join("");
    }
    function show(){
        container.html(printHead()+printBody()+printTail());
    }
    show();
    bindEvent();
}