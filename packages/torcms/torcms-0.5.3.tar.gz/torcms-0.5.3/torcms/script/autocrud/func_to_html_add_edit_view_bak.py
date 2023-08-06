# -*- coding:utf-8 -*-
def gen_input_add(sig):
    html_fangjia = '''
     <div class="form-group">
    <label class="col-sm-2 control-label" for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span></label>
<div class="col-sm-10">
    <input id='{0}' name="{0}" value="" type="text"  class="form-control"> {2}</div></div>
    '''.format(sig['en'], sig['zh'], sig['dic'][1])
    return (html_fangjia)


def gen_input_edit(sig):
    edit_fangjia = '''
     <div class="form-group">
    <label class="col-sm-2 control-label" for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a>{1}</span></label>
<div class="col-sm-10">
    <input id='{0}' name="{0}" value="{{{{ post_info.extinfo['{0}'][0] }}}}" type="text"  class="form-control"> {2}</div></div>
    '''.format(sig['en'], sig['zh'], sig['dic'][1])
    return (edit_fangjia)


def gen_input_view(sig):
    out_str = '''
    <div class="col-sm-4"><span class="des">{1}</span></div>
    <div class="col-sm-8"><span class="val">{{{{ post_info.extinfo['{0}'][0] }}}} {2}</span></div>
    '''.format(sig['en'], sig['zh'], sig['dic'][1])
    return (out_str)


def gen_radio_add(sig):
    html_zuoxiang = '''
    <div class="form-group">
    <label class="col-sm-2 control-label" for="{0}"><span style="color:red">*</span>{1}</label>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''<div class="col-sm-10">
        <input id="{0}" name="{0}" type="radio"  class="form-control" value="{1}">{2}
        </div>'''.format(sig['en'], key, dic_tmp[key])
        html_zuoxiang += tmp_str

    html_zuoxiang += '''</div>'''
    return (html_zuoxiang)


def gen_radio_edit(sig):
    edit_zuoxiang = '''
    <div class="form-group">
    <label class="col-sm-2 control-label" for="{0}"><span style="color:red">*</span>{1}</label>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''<div class="col-sm-10">
        <input id="{0}" name="{0}" type="radio"  class="form-control" value="{1}"
        {{% if post_info.extinfo['{0}'][0] == '{1}' %}}
        checked
        {{% end %}}
        >{2}</div>'''.format(sig['en'], key, dic_tmp[key])
        edit_zuoxiang += tmp_str

    edit_zuoxiang += '''</div>'''
    return (edit_zuoxiang)


def gen_radio_view(sig):
    view_zuoxiang = '''
    <div class="col-sm-4"><span class="des">{0}</span></div>
    <div class="col-sm-8">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span class="form-control">
         {{% if post_info.extinfo['{0}'][0] == "{1}" %}}
         {2}
         {{% end %}}
         </span>
        '''.format(sig['en'], key, dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return (view_zuoxiang)


def gen_checkbox_add(sig):
    html_wuneisheshi = '''
    <div class="form-group">
    <label class="col-sm-2 control-label" for="{0}"><span style="color:red">*</span>{1}</label>
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''<div class="col-sm-10">
        <input id="{0}" name="{0}" type="checkbox" class="form-control" value="{1}">{2}
        </div>'''.format(sig['en'], key, dic_tmp[key])
        html_wuneisheshi += tmp_str

    html_wuneisheshi += '''</div>'''
    return (html_wuneisheshi)


def gen_checkbox_edit(sig):
    edit_wuneisheshi = '''
     <div class="form-group">
     <label class="col-sm-2 control-label" for="{0}"><span style="color:red">*</span>{1}</label>
     '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''<div class="col-sm-10">
         <input id="{0}" name="{0}" type="checkbox" class="form-control" value="{1}"
         {{% if "{1}" in post_info.extinfo["{0}"] %}}
         checked="checked"
         {{% end %}}
         >{2}</div>'''.format(sig['en'], key, dic_tmp[key])
        edit_wuneisheshi += tmp_str

    edit_wuneisheshi += '''</div>'''
    return (edit_wuneisheshi)


def gen_checkbox_view(sig):
    view_zuoxiang = '''
    <div class="col-sm-4"><span class="des">{0}</span></div>
    <div class="col-sm-8">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span>
         {{% if "{0}" in post_info.extinfo["{1}"] %}}
         {2}
         {{% end %}}
         </span>
         '''.format(key, sig['en'], dic_tmp[key])
        view_zuoxiang += tmp_str

    view_zuoxiang += '''</div>'''
    return (view_zuoxiang)


def gen_select_add(sig):
    html_jushi = '''
 <div class="form-group">

    <label class="col-sm-2 control-label" for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span></label>
<div class="col-sm-10">
    <select id="{0}" name="{0}" class="form-control">
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']

    for key in dic_tmp.keys():
        tmp_str = '''
        <option value="{1}">{2}</option>
        '''.format(sig['en'], key, dic_tmp[key])
        html_jushi += tmp_str

    html_jushi += '''</select> </div></div> '''
    return (html_jushi)


def gen_select_edit(sig):
    edit_jushi = '''
<div class="form-group">
   <label class="col-sm-2 control-label" for="{0}"><span><a class="glyphicon glyphicon-star" style="color: red;font-size: xx-small;"></a> {1}</span></label>
<div class="col-sm-10">
    <select id="{0}" name="{0}" class="form-control">
    '''.format(sig['en'], sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''        
        <option value="{1}"
        {{% if post_info.extinfo["{0}"][0] == "{1}" %}}
        selected = "selected"
        {{% end %}}
        >{2}adadfadf</option>
        '''.format(sig['en'], key, dic_tmp[key])
        edit_jushi += tmp_str

    edit_jushi += '''</select></div></div>  '''
    return (edit_jushi)


def gen_select_view(sig):
    view_jushi = '''
    <div class="col-sm-4"><span class="des">{0}</span></div>
    <div class="col-sm-8">
    '''.format(sig['zh'])

    dic_tmp = sig['dic']
    for key in dic_tmp.keys():
        tmp_str = '''
         <span>
          {{% set tmp_var = post_info.extinfo["{0}"][0] %}}
          {{% if tmp_var == "{1}" %}}
          {2}
          {{% end %}}
         </span>
         '''.format(sig['en'], key, dic_tmp[key])
        view_jushi += tmp_str

    view_jushi += '''</div>'''
    return (view_jushi)


def gen_file_add(sig):
    add_html = '''
    <div class="form-group">
    <label class="col-sm-2 control-label" for="dasf">上传图片：</label>
    <div id="dasf" class="col-sm-10"> png,jpg,gif,jpeg格式！大小不得超过500KB </div>
    </div>
    <div class="form-group" >
    <label for="mymps_img2" class="col-sm-2 control-label"> </label>
    <div id="mymps_img2" class="col-sm-10">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img1">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img3">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img4">
    </div>
    </div>
    '''
    return (add_html)


def gen_file_view(sig):
    view_html = ''
    return (view_html)


def gen_file_edit(sig):
    view_html = '''
    <div class="form-group">
    <label for="dasf">上传图片：</label>
    <div id="dasf" class="col-sm-10"> png,jpg,gif,jpeg格式！大小不得超过500KB </div>
    </div>
    <div class="form-group">
    <label for="mymps_img2" class="col-sm-2 control-label"> </label>
    <div id="mymps_img2" class="col-sm-10">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img1">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img2">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img3">
    <input class="pure-button" type="file" name="mymps_img" id="mymps_img4">
    </div>
    </div>
    '''
    return (view_html)
