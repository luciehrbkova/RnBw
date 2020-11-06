// _____________________dropdown menu_______________________________ 

function openNav() 
    {
        document.getElementById("dropdown_menu").style.display = "block";
        document.getElementById("menu_img").src = "static/img/close_menu.png";
        document.getElementById("btn_menu").setAttribute("onClick", "closeNav()");
    }

    function closeNav() 
    {
        document.getElementById("dropdown_menu").style.display = "none";
        document.getElementById("menu_img").src = "{{ url_for('static', filename='static/img/menu.png') }}";
        document.getElementById("btn_menu").setAttribute("onClick", "openNav()");
    }
