/**
 * Created by Abdul on 6/20/2016.
 */

function delete_user(user_id,url_path){
   if(confirm("This action will delete user and its all images."))
   {
       window.open("/panel/del_user?user_id="+user_id+"&redirect_url="+url_path,"_self")
   }
   }

function delete_ratings(user_id,url_path){
   if(confirm("This action will delete user's all ratings."))
   {
       window.open("/panel/del_ratings?user_id="+user_id+"&redirect_url="+url_path,"_self")
   }
   }

function populate_modal(user_id,redirect_url){
    $.get( "/panel/get_user?user_id="+user_id, function( data ) {
        data = JSON.parse(data,removeNulls)
        if(!$.isEmptyObject(data)){
                   $("#editModalBody").empty();
                   $("#editModalBody").append('<div class="form-group"><label>Name</label><input class="form-control" placeholder="Enter Name" name="name" value='+data.name+'></div>' +
                   '<div class="form-group"><label>City</label><input class="form-control" placeholder="Enter City" name="city" value='+data.city+'></div>' +
                   '<div class="form-group"><label>Age</label><input type="number" class="form-control" placeholder="Enter Age" name="age" value='+data.age+' min="18" max="100"></div>' +
                   '<div class="form-group"><label>Password</label><input class="form-control" placeholder="Enter Password" name="password" value='+data.password+'></div>' +
                   '<div class="form-group"><label>Profile Rating</label><input min="0" max="5" type="number" step="0.1" class="form-control" id="profile_rating" name="profile_rating" value='+data.profile_rating+'></div>' +
                   '<div class="form-group"><label>Email</label><p class="form-control-static" id="email">'+data.email+'</p></div>' +
                   '<div class="form-group"><div class="checkbox"><label><input type="checkbox" id="is_approved" name="is_approved">Is Approved</label></div>' +
                   '<div class="checkbox"><label><input type="checkbox" id="is_public" name="is_public">Is Public</label></div>' +
                   '<div class="checkbox"><label><input type="checkbox"  id="is_active" name="is_active">Is Active</label></div></div>'+
                   '<div class=""><input type="hidden"  id="user_id" value='+data.id+' name="user_id"></div></div>'+
                   '<div class=""><input type="hidden"  id="redirect_url" value='+redirect_url+' name="redirect_url"></div></div>'
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



function populate_images(user_id){
    $.get( "/panel/get_images?user_id="+user_id, function( data ) {
        data = JSON.parse(data,removeNulls)
        if(!$.isEmptyObject(data)){
                   $("#imgModalBody").empty();
                    for(d in data){
                   $("#imgModalBody").append('<div class="col-xs-4"><div class="form-group"><img src="'+data[d].img_url+'" alt="User Images" style="width:150px;height:250px;"></div></div></div>')
                    }

               }
        else{
                   $("#imgModalBody").empty();
                   $("#imgModalBody").append('<div class="alert alert-info alert-dismissable">User has not uploaded any image yet.</div>')

               }



           });
}


function populate_users(contest_id){
    $.get( "/panel/get_contest_users?contest_id="+contest_id, function( data ) {
        $("#userModalBody").empty();
        $("#userModalBody").append(data)
    });

}




function post_form(){
      $("#form_update_user").submit()
 }