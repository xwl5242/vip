$(function(){
    //视频播放源点击功能
    $('.tv-source a').click(function(){
        $('.tv-source a').removeClass('fed-back-green');
        $(this).addClass('fed-back-green');
        let tv_source = $(this).parent().attr('data-tv-source');
        tv_source = "data-tv-source-"+tv_source;
        $('ul[class^="data-tv-source-"]').hide();
        $('ul').filter("."+tv_source).show();
    });
    //视频排序功能
    $('.tv-order').toggle(function(){
        $(this).html('视频排序：倒序');
        let tv_source = $('.tv-source a').filter('.fed-back-green').parent().attr('data-tv-source');
        tv_source = "data-tv-source-"+tv_source;
        $('ul[class^="data-tv-source-"]').hide();
        $('ul').filter("."+tv_source+'-r').show();
    },function(){
        $(this).html('视频排序：正序');
        let tv_source = $('.tv-source a').filter('.fed-back-green').parent().attr('data-tv-source');
        tv_source = "data-tv-source-"+tv_source;
        $('ul[class^="data-tv-source-"]').hide();
        $('ul').filter("."+tv_source).show();
    });
    //播放列表点击功能
    $('.tv_list').click(function(){
        $(this).addClass('fed-text-green');
        $('.tv_intro').removeClass('fed-text-green');
        $('.fed-tabs-boxs > div:eq(0)').show()
        $('.fed-tabs-boxs > div:eq(1)').removeClass('fed-text-green').hide()
    });
    //剧情介绍功能
    $('.tv_intro').click(function(){
        $(this).addClass('fed-text-green')
        $('.tv_list').removeClass('fed-text-green')
        $('.fed-tabs-boxs > div:eq(1)').addClass('fed-text-green').show()
        $('.fed-tabs-boxs > div:eq(0)').removeClass('fed-text-green').hide()
    });
});
//报错功能
function errseekmsg(){
    let tv_id = $(this).attr('data-tv-id');
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
                $.post('/err-seek-msg',{msg: tv_id+'@'+msg, m_type: '0'},function(data){
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
}