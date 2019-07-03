(function($){
	$(function(){
	    let my_theme_href = localStorage.getItem('my_theme_href');
	    if(my_theme_href){
	        top.$('#fed-colo-color').attr('href', my_theme_href);
        }
        $('#sx_switch').toggle(function(){
            $(this).html('视频排序：倒序')
            $('#zx_url').hide();
            $('#dx_url').show();
        },function(){
            $(this).html('视频排序：正序')
            $('#zx_url').show();
            $('#dx_url').hide();
        });
        $('#tv_list').click(function(){
            $(this).addClass('fed-text-green')
            $('#tv_intro').removeClass('fed-text-green')
            $('.fed-tabs-boxs > div:eq(0)').show()
            $('.fed-tabs-boxs > div:eq(1)').removeClass('fed-text-green').hide()
        });
        $('#tv_intro').click(function(){
            $(this).addClass('fed-text-green')
            $('#tv_list').removeClass('fed-text-green')
            $('.fed-tabs-boxs > div:eq(1)').addClass('fed-text-green').show()
            $('.fed-tabs-boxs > div:eq(0)').removeClass('fed-text-green').hide()
        });

        var mySwiper = new Swiper('.fed-swip-container', {
            wrapperClass: 'fed-swip-wrapper',
            slideClass: 'fed-swip-slide',
            slideNextClass: 'fed-swip-next',
            slidePrevClass: 'fed-swip-prev',
            autoplay: true,//可选选项，自动滑动
        })

        //设置页面顶端的导航选中状态
        let h = window.location.href.split('//')[1].replace('/', '')
        if(h == window.location.host){
            localStorage.setItem('selected_nav_id', 'nav_li_1')
        }
        let sel_nav_id = localStorage.getItem('selected_nav_id');
        sel_nav_id =  (sel_nav_id&&sel_nav_id!='undefined')?sel_nav_id:'nav_li_1'
        $('#'+sel_nav_id).find('a').removeClass('fed-text-green').addClass('fed-text-green')
        $('.p-id-'+sel_nav_id).removeClass('fed-this').addClass('fed-this')
        //页面右侧滚动到页面顶部相关
        window.onscroll= function(){
            //变量t是滚动条滚动时，距离顶部的距离
            let t = document.documentElement.scrollTop||document.body.scrollTop;
            if(t>=400){
                $(".fed-goto-toper").removeClass('fed-hidden').addClass('fed-visible')
            }else{
                $(".fed-goto-toper").removeClass('fed-visible').addClass('fed-hidden')
            }
        }
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
        })
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
        //换肤
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
        //报错
        $('.fed-tabs-errs').click(function(){
            layer.open({
                title: '报错',
                content: $('#err_seek_msg').html(),
                btn: ['提交', '取消'],
                success: function(layero, index){
                    $(layero).find('textarea').attr('placeholder','请输入200字以内的错误信息，谢谢！');
                },
                btn1: function(index, layero) {
                    let msg = $(layero).find('textarea').val()
                    if (msg) {
                        $.post('/err-seek-msg',{msg: msg, m_type: '0'},function(data){
                            if(data.code=='success'){
                                layer.close(index);
                                layer.msg('提交成功！我们会尽快处理，谢谢！');
                            }
                        },'json');
                    } else {
                        layer.tips('请先填写错误信息！', '.layui-layer-btn0', {tips: 1});
                        return false;
                    }
                },
                btn2: function(index, layero){
                    layer.close(index);
                }
            })
        });
    });
})(jQuery);
