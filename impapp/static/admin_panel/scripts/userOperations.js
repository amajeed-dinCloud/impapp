/**
 * Created by Abdul on 6/20/2016.
 */

function delete_user(user_id){
   if(confirm("This action will delete user and its all images."))
   {
       var url_path = "{{ request.path }}"
       window.open("/panel/del_user?user_id="+user_id+"&redirect_url="+url_path,"_self")
   }
   }

function populate_modal(user_id){
    $.get( "/panel/get_user?user_id="+user_id, function( data ) {
        data = JSON.parse(data,removeNulls)
        if(!$.isEmptyObject(data)){
                   $("#editModalBody").empty();
                   $("#editModalBody").append('<div class="form-group"><label>Name</label><input class="form-control" placeholder="Enter Name" name="name" value='+data.name+'></div>' +
                   '<div class="form-group"><label>City</label><input class="form-control" placeholder="Enter City" name="city" value='+data.city+'></div>' +
                   '<div class="form-group"><label>Age</label><input type="number" class="form-control" placeholder="Enter Age" name="age" value='+data.age+' min="18" max="100"></div>' +
                   '<div class="form-group"><label>Password</label><input class="form-control" placeholder="Enter Password" name="password" value='+data.password+'></div>' +
                   '<div class="form-group"><label>Profile Rating</label><p class="form-control-static" id="rating">'+data.profile_rating+'</p></div>' +
                   '<div class="form-group"><label>Email</label><p class="form-control-static" id="email">'+data.email+'</p></div>' +
                   '<div class="form-group"><div class="checkbox"><label><input type="checkbox" id="is_approved" name="is_approved">Is Approved</label></div>' +
                   '<div class="checkbox"><label><input type="checkbox" id="is_public" name="is_public">Is Public</label></div>' +
                   '<div class="checkbox"><label><input type="checkbox"  id="is_active" name="is_active">Is Active</label></div></div>'+
                   '<div class=""><input type="hidden"  id="user_id" value='+data.id+' name="user_id"></div></div>'+
                   '<div class=""><input type="hidden"  id="redirect_url" value="{{ request.path }}" name="redirect_url"><input type="hidden"  id="redirect_url" value="{{ request.path }}" name="redirect_url"></div></div>'
                   )

                   if(data.is_approved) $("#is_approved").prop('checked',true)
                   if(data.is_public) $("#is_public").prop('checked',true)
                   if(data.is_active)$("#is_active").prop('checked',true)

                   $("#editModalFooter").empty()
                   $("#editModalFooter").append('<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>' +
                   '<button type="button" class="btn btn-primary" onclick="post_form()">Update User</button>')
               }



           });
}

function removeNulls(key, value) {
   if (typeof value === 'object' && $.isEmptyObject(value)) {
        return ""
    }
    return value;
}

function post_form(){
    $("#form_update_user").submit()
}