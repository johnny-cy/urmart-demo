<script type="text/javascript">
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFToken'
    if (location.protocol=="https:"){
        var websocket_protocol = "wss://"
    } else {
        var websocket_protocol = "ws://"
    };
    
    const urmartSocket = new WebSocket(
        websocket_protocol
        + window.location.host
        + '/ws/urmart/update/'
    );

    urmartSocket.onmessage = function(e){
        const data = JSON.parse(e.data);
        const [r, c] = UpdateField(data.message.data)
        if (r){success_prompt(c, 2000)};
    };
    
    
    function GetProduct(pid=0){
        if (!is_ws_alive()){return}
        axios.get("{% url 'GetProduct' pid=0 %}".replace('0', pid))
            .then((response)=>{
                for (let i=0;i<response.data.results.length; i++){
                    let id = response.data.results[i].id;
                    let is_vip = response.data.results[i].Vip;
                    let ck = "";
                    if (is_vip){
                        ck = "checked";
                    };
                    // console.log(response)
                    $("#product-names").append('\
                    <option value='+ id +'>'+id +'</option>\
                    ');
                    $("#product-table>tbody").append('\
                    <tr name=pid-'+ id +'>\
                        <td name="pa">'+ response.data.results[i].id +'</td>\
                        <td name="pb">'+ response.data.results[i].Stock_pcs +'</td>\
                        <td name="pc">'+ response.data.results[i].Price +'</td>\
                        <td name="pd">'+ response.data.results[i].Shop_id_id +'</td>\
                        <td name="pe"> <input type="checkbox" '+ ck +' disabled> </td>\
                        <td></td>\
                    </tr>\
                    ');
                }
            }).catch((error)=>{
                console.log(error)
            });
    };

    function GetOrder(oid=0){
        if (!is_ws_alive()){return}
        axios.get("{% url 'GetOrder' oid=0 %}".replace("0", oid))
            .then((response)=>{
                // console.log(response)
                for (let i=0; i< response.data.results.length;i++){
                    $("#order-table>tbody").append("\
                    <tr name='oid-"+ response.data.results[i].id +"''>\
                        <td name='oa'> "+ response.data.results[i].id +" </td>\
                        <td name='ob'> "+ response.data.results[i].Product_id_id +" </td>\
                        <td name='oc'> "+ response.data.results[i].Qty +" </td>\
                        <td name='od'> "+ response.data.results[i].Shop_id +" </td>\
                        <td name='oe'> "+ response.data.results[i].Customer +" </td>\
                        <td > <div class='minus-circle' onclick='DelOrder("+(response.data.results[i].id)+")'>–</div> </td>\
                    </tr>\
                    ");
                };
            }).catch((error)=>{
                console.log(error)
            });
    };

    function AddOrder(){
        if (!is_ws_alive()){return}
        let pid = $("option:selected").attr('value');
        if (pid==='0'){
            alert("產品ID尚未選擇")
            $("#product-names").select()
            return
        };
        let qty = $('#amount').val()
        console.log("qty is ", qty)
        if (!qty|| qty==0){
            alert("添加的數量尚未填寫")
            $('#amount').select()
            return
        }
        let is_vip = $("#is_vip").prop("checked")
        if (!$('#cid').val()){
            alert("客戶的編號尚未填寫")
            $('#cid').select()
            return
        }
        if (confirm("確定要添加商品編號"+pid+"至訂單嗎？")){
            // console.log('confirm add pid'+pid)
        } else {
            return
        };
        let cid = $("#cid").val()
        axios.post("{% url 'AddOrder' %}", data={
                pid: pid,
                qty: qty,
                is_vip: is_vip,
                cid: cid
            })
            .then((response)=>{
                
                // update product stock_pcs
                message_info1 = {"veb":"update", "tgt": "pd", "tgtid": pid , "fld": "qty", "val": -qty}
                BroadcastGroup(message_info1)
                //update order table
                message_info2 = {"veb":"prepend", "tgt": "od", 
                    "tgtid": response.data.results[0].id, "fld":"all", 
                    "val": {
                        "Shop_id": response.data.results[0].Shop_id,
                        "Price": response.data.results[0].Price,
                        "Qty": response.data.results[0].Qty,
                        "Pid": response.data.results[0].Product_id_id,
                        "Customer": response.data.results[0].Customer,
                    }}
                console.log("廣播添加訂單列表")
                // console.log(message_info2)
                BroadcastGroup(message_info2)
            })
            .catch((error)=>{
                console.log(error.response.data.error_message)
                if (error.response.data.error_message == "insufficient stock."){
                    alert_error = "此商品庫存量不足"+qty+"件，當前只剩下"+error.response.data.current_stock+"件。"
                } else if(error.response.data.error_message == "vip-purchased only"){
                    alert_error = "此商品需要會員身分才能添加"
                } else {
                    alert_error = "發生未知的錯誤。"
                };
                alert(alert_error)
            });
    };

    function GetTop(num=3){
        if (!is_ws_alive()){return}
        axios.post("{% url 'GetTop' %}", data={
            num: num,
            // order_by: "",
            // order: "",
        })
        .then((response)=>{
            let alert_string = "依銷售量排行，\n\n"
            for (var i=0;i<response.data.results.length;i++){
                let pid = response.data.results[i].Product_id
                let sales = response.data.results[i].sales
                if (i==response.data.results.length-1){
                    alert_string += "而第"+(i+1)+"名產品編號"+pid+"，銷售數量則是"+sales+"件。"
                }else {
                    alert_string += "第"+(i+1)+"名產品編號"+pid+"，銷售數量"+sales+"件，"
                }
            };
            // console.log(response.data.results.length)
            if (response.data.results.length>0){
                console.log(alert_string);
                alert(alert_string);
            } else {
                err_string = "目前沒有訂單能統計"
                console.log(err_string);
                alert(err_string);
            };
        });
    };
    function DelOrder(oid){
        if (!is_ws_alive()){return}
        if (confirm("確定要刪除訂單編號"+oid+"嗎？")){
            // console.log('confirm delete oid'+oid)
        } else {
            return
        };
        axios.delete("{% url 'DelOrder' oid=999 %}".replace(999, oid))
            .then((response)=>{
                
                // RefreshOrder() // instead of refresh, delete specific order
                message_info = {"veb": "delete",
                    "tgt": "od",
                    "tgtid": oid,
                    "fld": "id",
                    "val": false}
                BroadcastGroup(message_info)
                // 前台再告訴大家將刪除訂單之庫存加回去商品
                message_info2 = {
                    "veb": "update", 
                    "tgt": "pd", 
                    "tgtid": response.data.results.Pid,
                    "fld": "qty",
                    "val": response.data.results.Qty
                }
                BroadcastGroup(message_info2)
            })
            .catch((error)=>{
                console.log(error)
            });
    };
    function RefreshOrder(){
        if (!is_ws_alive()){return}
        $("#order-table>tbody").empty();
        GetOrder();
    };

    function BroadcastGroup(data){
        is_ws_alive()
        urmartSocket.send(JSON.stringify({
            'message': {"data": data}
        }));
    };
    function UpdateField(data){
        if (data.tgt=="pd"){
            if (data.fld=="qty"){
                if (data.veb=="update"){
                    el = $("#product-table>tbody>tr[name='pid-"+ data.tgtid+"']>td[name='pb']") //pb is sotck_pcs
                    el.fadeOut("slow")
                    ori_val = parseInt(el.text())
                    new_val = (ori_val+data.val)
                    el.text(ori_val+data.val)
                    el.fadeIn("slow")
                    return [true, "商品編號"+ data.tgtid +"的存貨數量更新為"+ new_val +"。"]
                }
            };
        } else if(data.tgt=="od"){
            console.log("update field od")
            if (data.fld=="id"){
                if (data.veb=="delete"){
                    console.log("data fld id")
                    el = $("#order-table>tbody>tr[name='oid-"+ data.tgtid +"']").fadeOut("slow")
                    return [true, "訂單編號"+ data.tgtid +"被刪除，存貨已退回。"]
                }
            
            } else if (data.fld=="all"){
                console.log("in all")
                if (data.veb=="prepend"){
                    var t = $("\
                    <tr name='oid-"+ data.tgtid +"''>\
                        <td name='oa'> "+ data.tgtid +" </td>\
                        <td name='ob'> "+ data.val.Pid +" </td>\
                        <td name='oc'> "+ data.val.Qty +" </td>\
                        <td name='od'> "+ data.val.Shop_id +" </td>\
                        <td name='oe'> "+ data.val.Customer +" </td>\
                        <td > <div class='minus-circle' onclick='DelOrder("+(data.tgtid)+")'>–</div> </td>\
                    </tr>\
                    ").hide()
                    $("#order-table>tbody").prepend(t)
                    t.fadeIn("slow")

                    {% comment %} el = $("#order-table>tbody").prepend("\
                    <tr name='oid-"+ data.tgtid +"''>\
                        <td name='oa'> "+ data.tgtid +" </td>\
                        <td name='ob'> "+ data.val.Pid +" </td>\
                        <td name='oc'> "+ data.val.Qty +" </td>\
                        <td name='od'> "+ data.val.Shop_id +" </td>\
                        <td name='oe'> "+ data.val.Customer +" </td>\
                        <td > <div class='minus-circle' onclick='DelOrder("+(data.tgtid)+")'>–</div> </td>\
                    </tr>\
                    ").fadeIn("slow") {% endcomment %}
                    return [false, ""]
                };
            };
        };
    };
    function GenReport(){
        axios.get("{% url 'GenReport' %}")
            .then((response)=>{
                console.log(response.data.results)
                alert("Generating CSV Shop Report, please visit static file service as the following link 'https://ap3.test-vm.life/urmart/static/'")
            })
            .catch((error)=>{
                console.log(error)
            });
    };

    var prompt = function (message, style, time){
            style = (style === undefined) ? 'alert-success' : style;
            time = (time === undefined) ? 1200 : time;
            $('<div >')
                .prependTo('body')
                .addClass('alert ' + style)
                .html(message)
                .show()
                .delay(time)
                .fadeOut();
        };
    var success_prompt = function(message, time){
            prompt(message, 'alert-success', time);
        };
    
    var is_ws_alive = function(){
            if (urmartSocket.readyState == 2 || urmartSocket.readyState == 3){
                alert("WS服務器已斷開，將重新整理頁面。")
                location.reload(true);
                return false
            } else {
                return true
            };

        };
    $(document).ready(function(){
        $('#amount').bind('keyup paste', function(){
            this.value = this.value.replace(/^[^1-9]/g, ''); // replace none digits to empty
        });

        GetProduct()
        GetOrder()
        
        // GetTop()
    });

</script>
