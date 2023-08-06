quali_count = 1;
function AddMoreQuali() {
    var NewDiv = document.createElement("div");
    var NewId = "quali" + quali_count;
    
    NewDiv.innerHTML = "<br><div class=\"row form-group\">\
							<label class=\"control-label col-sm-2 col-sm-offset-2\">Name</label>\
							<div class=\"col-sm-6\">\
									<input class=\"form-control\" id=\"id_qualification_set-"+quali_count+"-name\" maxlength=\"100\" name=\"qualification_set-"+quali_count+"-name\" placeholder=\"Name\" required=\"True\" type=\"text\" />\
							</div>\
						</div>\
						<div class=\"row form-group\">\
							<label class=\"control-label col-sm-2 col-sm-offset-2\">Duration</label>\
							<div class=\"col-sm-6\">\
									<input class=\"form-control\" id=\"id_qualification_set-"+quali_count+"-duration\" name=\"qualification_set-"+quali_count+"-duration\" placeholder=\"Duration\" required=\"True\" type=\"number\" />\
							</div>\
						</div>\
						<div class=\"row form-group\">\
							<label class=\"control-label col-sm-2 col-sm-offset-2\">Board</label>\
							<div class=\"col-sm-6\">\
									<input class=\"form-control\" id=\"id_qualification_set-"+quali_count+"-board\" maxlength=\"100\" name=\"qualification_set-"+quali_count+"-board\" placeholder=\"Board\" required=\"True\" type=\"text\" />\
							</div>\
						</div>\
						<div class=\"row form-group\">\
							<label class=\"control-label col-sm-2 col-sm-offset-2\">Marks</label>\
							<div class=\"col-sm-6\">\
									<input class=\"form-control\" id=\"id_qualification_set-"+quali_count+"-marks\" name=\"qualification_set-"+quali_count+"-marks\" placeholder=\"Marks\" required=\"True\" step=\"any\" type=\"number\" />\
							</div>\
						</div>\
						<div class=\"row form-group\"><button type=\"button\" class=\"btn btn-default col-sm-2 col-sm-offset-8\" onClick=\"javascript:removeQuali("+quali_count+")\">Remove</button></div>";
    NewDiv.id = NewId;
    
    $new_div=$(NewDiv);
    $new_div.hide()
    $exp_div=$('#quali');
    $exp_div.append($new_div);
    $new_div.show('slow');
    quali_count++;
    $('#id_qualification_set-TOTAL_FORMS').val(quali_count);
     $('#add_quali_btn').blur();
}

exp_count = 1;
function AddMoreExp() {
    var exp_div = document.getElementById("exp");
    var NewDiv = document.createElement("div");
    var NewId = "exp" + exp_count;
    
    NewDiv.innerHTML = "<br><div class=\"row form-group\"><label class=\"control-label col-sm-2 col-sm-offset-2\">Exp title</label><div class=\"col-sm-6\"><input class=\"form-control\" id=\"id_experience_set-"+exp_count+"-exp_title\" maxlength=\"100\" name=\"experience_set-"+exp_count+"-exp_title\" placeholder=\"Exp title\" required=\"True\" type=\"text\" /></div></div><div class=\"row form-group\"><label class=\"control-label col-sm-2 col-sm-offset-2\">Duration</label><div class=\"col-sm-6\"><input class=\"form-control\" id=\"id_experience_set-"+exp_count+"-duration\" name=\"experience_set-"+exp_count+"-duration\" placeholder=\"Duration\" required=\"True\" type=\"number\" /></div></div><div class=\"row form-group\"><label class=\"control-label col-sm-2 col-sm-offset-2\">Summary</label><div class=\"col-sm-6\"><input class=\"form-control\" id=\"id_experience_set-"+exp_count+"-summary\" maxlength=\"200\" name=\"experience_set-"+exp_count+"-summary\" placeholder=\"Summary\" required=\"True\" type=\"text\" /></div></div><div class=\"row form-group\"><button type=\"button\" class=\"btn btn-default col-sm-2 col-sm-offset-8\" onClick=\"javascript:removeExp("+exp_count+")\">Remove</button></div></div>";
    NewDiv.id = NewId;
    
    $new_div=$(NewDiv);
    $new_div.hide()
    $exp_div=$('#exp');
    $exp_div.append($new_div);
    $new_div.show('slow');
    exp_count++;
    $('#id_experience_set-TOTAL_FORMS').val(exp_count);
    $('#add_exp_btn').blur();
}
function removeExp(pos) {
	var id="exp"+pos;
	var main=document.getElementById("exp");
    var removed=false;
    console.log(main.children.length);
    var children=main.children;
    for(var i=0;i<children.length;i++)
	{
		var childDiv=children[i];
		console.log(childDiv.id);
		if(childDiv.id===id){
			console.log("removed");
			removed=true;
			
		}else{
			if(removed){
				console.log("set "+(i-1));
				childDiv.id='exp'+(i-1);
				var inputs=childDiv.getElementsByTagName('input');
				for(var j=0;j<inputs.length;j++){
					var input=inputs[j];
					
					var idarr=input.id.split('-');
					idarr[1]=''+(i-1);
					input.id=idarr[0]+'-'+idarr[1]+'-'+idarr[2];
					
					var namearr=input.name.split('-');
					namearr[1]=''+(i-1);
					input.name=namearr[0]+'-'+namearr[1]+'-'+namearr[2];
				}
				var rmbtn=childDiv.getElementsByTagName('button')[0];
				console.log('before btn-'+rmbtn.onclick);
				rmbtn.setAttribute('onclick','javascript:removeExp('+(i-1)+')');
				console.log('after btn-'+rmbtn.onclick);
			}
			else
				console.log("not removed");
		}
	}
	exp_count--;
	 $('#id_experience_set-TOTAL_FORMS').val(exp_count);
	id='#'+id;
	$target=$(id);
	$target.hide('slow', function(){ $target.remove(); });
	//main.removeChild();
    
}

function removeQuali(pos) {
    var id="quali"+pos;
	var main=document.getElementById("quali");
    var removed=false;
    console.log(main.children.length);
    var children=main.children;
     for(var i=0;i<children.length;i++)
	{
		var childDiv=children[i];
		console.log(childDiv.id);
		if(childDiv.id===id){
			console.log("removed");
			removed=true;
			
		}else if(removed){
				console.log("set "+(i-1));
				childDiv.id='quali'+(i-1);
				var inputs=childDiv.getElementsByTagName('input');
				for(var j=0;j<inputs.length;j++){
					var input=inputs[j];
					
					var idarr=input.id.split('-');
					idarr[1]=''+(i-1);
					input.id=idarr[0]+'-'+idarr[1]+'-'+idarr[2];
					
					var namearr=input.name.split('-');
					namearr[1]=''+(i-1);
					input.name=namearr[0]+'-'+namearr[1]+'-'+namearr[2];
				}
				var rmbtn=childDiv.getElementsByTagName('button')[0];
				console.log('before btn-'+rmbtn.onclick);
				rmbtn.setAttribute('onclick','javascript:removeQuali('+(i-1)+')');
				console.log('after btn-'+rmbtn.onclick);
			}
		else
			console.log("not removed");
		
	}
    quali_count--;
    $('#id_qualification_set-TOTAL_FORMS').val(quali_count);
    id='#'+id;
	$target=$(id);
	$target.hide('slow', function(){ $target.remove(); });
}
