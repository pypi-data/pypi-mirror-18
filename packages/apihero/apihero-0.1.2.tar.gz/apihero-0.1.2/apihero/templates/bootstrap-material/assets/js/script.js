    /** functions **/
    function syntaxHighlight(json) {
        if (typeof json != 'string') {
                json = JSON.stringify(json, undefined, 2);
        }
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            var cls = 'number';
            if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'key';
                    } else {
                        cls = 'string';
                    }
            } else if (/true|false/.test(match)) {
                    cls = 'boolean';
            } else if (/null/.test(match)) {
                    cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    }

    function IsJsonString(str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }

    function replace_testunit_url_params(input_el){
        var parent = input_el.parents('.panel');
        var url_el = parent.find(".unit-url-replace");
        var url = url_el.attr('data-url');
        var new_val = url;
        parent.find('input').each(function(){
            if($(this).attr('name')!=undefined){
                new_val = new_val.replace(':'+$(this).attr('name'), $(this).val());
            }
        });
        url_el.text(new_val);
    }

    $(document).ready(function(){
        $('.testunit input').keyup(function(){
            replace_testunit_url_params($(this));
        });

        $('.testunit input').each(function(){
            replace_testunit_url_params($(this));
        });

        $('.testunit').submit(function(){
                var src_action = $(this).attr('src-action');
                var cur_action = src_action;
                var method = $(this).attr('method');

                // replace parameter values in url for GET method
                // e.g:
                // http://localhost/test/api/1/users/search/:keyword
                // replace with: http://localhost/test/api/1/users/search/john
                $(this).find('.in_action input').each(function(){
                    cur_action = cur_action.replace(':'+$(this).attr('name'),$(this).val());
                });

                $(this).attr('action', cur_action);
                var postData = new FormData(this);
                if (method=="get" || method=="GET"){
//                    actionstr =  actionstr + '?' + $(this).serialize();
                    postData = $(this).serialize();
                }
                var actionstr = $(this).attr("action");
                var rr = $.ajax({
                    url : actionstr,
                    type: method,
                    data : postData,
                    processData: false,
                    contentType: false,
                    success:function(data, textStatus, jqXHR){},
                    complete: function(data){
                        console.log(data.getAllResponseHeaders());
                        headers = "";
                        headers = data.getAllResponseHeaders();
                        data = data.responseText;
                        if (typeof data === 'object' || IsJsonString(data)) {
                            var response = JSON.stringify( JSON.parse(data), null, 2);
                        }else{
                            var response = data;
                        }
                        console.log(data);

                        var html = '';
                        html += '<div class="modal fade in" tabindex="-1">';
                        html += '<div class="modal-dialog modal-lg" style="width:900px;">';
                        html += '<div class="modal-content">';
                        html += '<div class="modal-header">';
                        html += '';
                        html += '<h4><a class="close" data-dismiss="modal">×</a>Result</h4>'
                        html += '</div>';
                        html += '<div class="modal-body">';
                        html += '<h5>Response Header</h5><pre class="unit-response-header" >'+headers+'</pre>';
                        html += '<h5>Response Body</h5>';
                        html += '<textarea class="form-control unit-response" readonly>'+response+'</textarea>';
                        html += '</div>';
                        html += '</div>';  // content
                        html += '</div>';  // dialog
                        html += '</div>';  // modal
                        $(html).modal();
                    }
                });

                return false;
        });
    });
