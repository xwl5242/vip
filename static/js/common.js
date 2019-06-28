$(function(){
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
})