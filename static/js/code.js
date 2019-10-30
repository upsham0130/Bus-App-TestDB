document.getElementById("signup").onclick = function(){
    forward();
    activate(document.getElementById("navsign"),"../static/img/boardY.png");
}
document.getElementById("routes").onclick = function(){
    forward()
    activate(document.getElementById("navroute"),"../static/img/mapY.png");
}
document.getElementById("navroute").onclick = function(){
    if(activated!="navroute"){
    deactivate(document.getElementById("navsign"),"../static/img/board.png");
    activate(document.getElementById("navroute"),"../static/img/mapY.png");
    }
}
document.getElementById("navsign").onclick = function(){
    if(activated!="navsign"){
    deactivate(document.getElementById("navroute"),"../static/img/map.png");
    activate(document.getElementById("navsign"),"../static/img/boardY.png");
    }
}
document.getElementById("bar").onclick = function(){
    back()
    deactivate(document.getElementById("navroute"),"../static/img/map.png");
    deactivate(document.getElementById("navsign"),"../static/img/board.png");
}
for(i=0;i<2;i++){
    document.getElementsByClassName("ArrowLeft")[i].onclick = function(){
        if(activated=="navsign"){
            if(signup_bus>1){
                signup_bus--;
                update_bus("sBus",signup_bus);
            }
        }
        else if(activated=="navroute"){
            if(route_bus>1){
                update_route(route_bus,route_pg,"hidden");
                route_bus--;
                update_bus("rBus",route_bus);
                route_pg = 0;
                update_route(route_bus,route_pg,"visible");
            }
        }
    }
    document.getElementsByClassName("ArrowRight")[i].onclick = function(){
        if(activated=="navsign"){
            if(signup_bus<3){
                signup_bus++;
                update_bus("sBus",signup_bus);
            }
        }
        else if(activated=="navroute"){
            if(route_bus<3){
                update_route(route_bus,route_pg,"hidden");
                route_bus++;
                update_bus("rBus",route_bus);
                route_pg = 0;
                update_route(route_bus,route_pg,"visible");
            }
        }
    }
} 
document.getElementById("next").onclick = function(){
    if(route_pg<document.getElementsByClassName("bus"+route_bus).length-1){
        update_route(route_bus,route_pg,"hidden");
        route_pg++;
        update_route(route_bus,route_pg,"visible");
    }
}
document.getElementById("back").onclick = function(){
    if(route_pg>0){
        update_route(route_bus,route_pg,"hidden");
        route_pg--;
        update_route(route_bus,route_pg,"visible");
    }
}
    
var debounce = false;
var activated = "";
var signup_bus = 0;
var route_bus = 1;
var route_pg = 0;

update_bus = function(e,num){
    if(num>0){
        document.getElementById(e).innerText = "Bus "+num;
    }
    else{document.getElementById(e).innerText = "--Select a Bus--"}
}
update_route = function(routenum,pg,status){
    document.getElementsByClassName("bus"+routenum)[pg].style.visibility = status;
}
forward = function(){
    if(!debounce){
        debounce = true;
        var  c1 = document.getElementById("hub").childNodes;
        for(i=0;i<c1.length;i++){
            var c2 = c1[i].childNodes;
            for(j=0;j<c2.length;j++){
            move(c2[j],1500,0,100);
            }
        }
        move(document.getElementsByClassName("side")[0],1300,-1710,100);
        move(document.getElementById("bird"),300,screen.width*.5,100);
        setTimeout(()=>move(document.getElementsByClassName("nav")[0],2000,-975,100,4),250);
        /*RRRYYYYISSEEE AND SHYYYYINEEEE */
        /*setTimeout(()=>move(document.getElementsByClassName("side")[0],1300,-1710,100),0);
        setTimeout(()=>move(document.getElementById("bird"),300,screen.width*.5,100),0); (sorry for flexing :/)*/
    }
}
change = function(el,s,col){
    if(el.id != activated){
        el.src = s;
        if(col){el.style.borderColor = "#E3BA41";}
        else if(col==false){el.style.borderColor = "#6D8BC9";}
        for(i=0;i<el.childNodes.length;i++){
            el.childNodes[i].src = s;
            if(col){el.childNodes[i].style.borderColor = "#E3BA41";}
            else if(col==false){el.childNodes[i].style.borderColor = "#6D8BC9";}
        }
    }
}
activate = function(el,s){
    if(el.id!=activated){
        document.getElementById(el.id+"_pg").style.visibility = "visible";
        activated = el.id;
        el.src = s;
        el.style.borderColor = "#E3BA41";
        //update bus
        update_route(route_bus,route_pg,"hidden");
        signup_bus = 0;
        route_bus = 1;
        route_pg = 0;
        update_bus("rBus",route_bus);
        update_bus("sBus",signup_bus);
        if(el.id=="navroute"){
            update_route(route_bus,route_pg,"visible");
        }
    }
}
deactivate = function(el,s){
    activated = "";
    el.src = s;
    el.style.borderColor = "#6D8BC9";
    document.getElementById(el.id+"_pg").style.visibility = "hidden";
}
back = function(){
    if(!debounce){
        debounce = true;
        move(document.getElementsByClassName("side")[0],-1300,-410,100);
        move(document.getElementById("bird"),-300,(screen.width*.5)+300,100);
        document.getElementsByClassName("nav").zIndex = "2";
        setTimeout(()=>move(document.getElementsByClassName("nav")[0],-2000,1025,100),50);
        var  c1 = document.getElementById("hub").childNodes;
        for(i=0;i<c1.length;i++){
            var c2 = c1[i].childNodes;
            for(j=0;j<c2.length;j++){
                move(c2[j],-1500,1500,100);
            }
        }
    }
}

move = function(el,num,current,pos,z){
    el.style = ";";
    var x = current+(num*pos/5050);
    el.style.left = x+"px";
    
    if(pos>=0){
        setTimeout(()=>move(el,num,x,pos-1,z),5);
    }
    else{
        debounce = false;
        if(Number.isInteger(z)){el.style.zIndex= z;}
    }
}
/*left:-410  top:-313*/