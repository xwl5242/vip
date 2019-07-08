(function($){
	$(function(){
	    //主题颜色，主题样式风格
	    let my_theme_href = localStorage.getItem('my_theme_href');
	    if(my_theme_href){
	        top.$('#fed-colo-color').attr('href', my_theme_href);
        }
        //换肤功能
        $('.fed-goto-color').click(function(){
            layer.open({
                title: '换肤',
                content: $('#color').html(),
                success: function(layero, index){
                    $(layero).find('.layui-layer-content li').click(function(){
                        let color_css = $(this).find('a').attr('data-type');
                        let old_css = top.$('#fed-colo-color').attr('href');
                        let prefix = old_css.substring(0, old_css.indexOf('css/')+4);
                        let subffix = old_css.substring(old_css.indexOf('.css'));
                        let new_css = prefix+color_css+subffix;
                        localStorage.setItem('my_theme_href', new_css);
                        top.$('#fed-colo-color').attr('href', new_css)
                    });
                }
            })
        });
	    //轮播效果
        let mySwiper = new Swiper('.fed-swip-container', {
            wrapperClass: 'fed-swip-wrapper',
            slideClass: 'fed-swip-slide',
            autoplay: true,//可选选项，自动滑动
        });

        //设置页面顶端的导航选中状态
        let h = window.location.href.split('//')[1].replace('/', '');
        if(h == window.location.host){
            localStorage.setItem('selected_nav_id', 'nav_li_1');
        }
        let sel_nav_id = localStorage.getItem('selected_nav_id');
        sel_nav_id =  (sel_nav_id&&sel_nav_id!='undefined')?sel_nav_id:'nav_li_1';
        $('#'+sel_nav_id).find('a').removeClass('fed-text-green').addClass('fed-text-green');
        $('.p-id-'+sel_nav_id).removeClass('fed-this').addClass('fed-this');

        //页面右侧滚动到页面顶部相关
        window.onscroll= function(){
            //变量t是滚动条滚动时，距离顶部的距离
            let t = document.documentElement.scrollTop||document.body.scrollTop;
            if(t>=400){
                $(".fed-goto-toper").removeClass('fed-hidden').addClass('fed-visible')
            }else{
                $(".fed-goto-toper").removeClass('fed-visible').addClass('fed-hidden')
            }
        };
        $('.fed-goto-toper').click(function(){
            $('html,body').animate({scrollTop: '0px'}, 800);
        });

        //导航栏，导航相关
        $('.fed-menu-info>li:last>a').click(function(){
            if($('.fed-pops-navbar').hasClass('fed-hidden')){
                $('.fed-pops-navbar').removeClass('fed-hidden').addClass('fed-visible')
            }else{
                $('.fed-pops-navbar').removeClass('fed-visible').addClass('fed-hidden')
            }
        });
        $('body > div:eq(1)').click(function(){
            $('.fed-pops-navbar').removeClass('fed-visible').addClass('fed-hidden');
            $('.fed-pops-search').removeClass('fed-visible').addClass('fed-hidden');
        });

        //搜索框，搜索相关
        $('.fed-navs-search input').click(function(){
            if($('.fed-pops-search').hasClass('fed-hidden')){
                $('.fed-pops-search').removeClass('fed-hidden').addClass('fed-visible');
            }else{
                $('.fed-pops-search').removeClass('fed-visible').addClass('fed-hidden');
            }
        });
        $('#index_ser_web_btn').click(function(){
            if($('.fed-navs-search').hasClass('fed-hidden')){
                $('.fed-navs-search').removeClass('fed-hidden').addClass('fed-visible');
            }else{
                $('.fed-navs-search').removeClass('fed-visible').addClass('fed-hidden');
            }
            if($('.fed-pops-search').hasClass('fed-hidden')){
                $('.fed-pops-search').removeClass('fed-hidden').addClass('fed-visible');
            }else{
                $('.fed-pops-search').removeClass('fed-visible').addClass('fed-hidden');
            }
        });
        //设置导航被选中样式相关
        $('.fed-menu-info > li').click(function(){
            localStorage.setItem('selected_nav_id', $(this).attr('id'));
        });
        $('.fed-pops-navbar li').click(function(){
            localStorage.setItem('selected_nav_id', $(this).attr('data-p-id'));
        });
        //搜索功能
        $('#index_ser_btn,#index_ser_web_btn').click(function(){
            let k = $(this).siblings('input').val();
            if(k){
               window.location.href = '/t-t/k='+ k;
            }
        });
        $('.fed-navs-record').click(function(){
            layer.open({
                title: '免责声明',
                content: $('#declare_content').html()
            });
        });
    });
})(jQuery);
