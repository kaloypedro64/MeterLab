let table_meters;

window.onload = function ()
{

    var AREA_CHOICES = [
        "Dipolog Main Office",
        "Piñan Area Services",
        "Sindangan Area Services",
        "Liloy Area Services"];

    function Load_serials_table()
    {
        table_meters = $('#table_meters').DataTable({
            "searching": true,
            "processing": true,
            "stateSave": true,
            "info": true,
            "paging": true,
            "lengthChange": true,
            "autoWidth": false,
            "responsive": true,
            "columnDefs": [
                { "targets": [0], "searchable": false, "orderable": false, "visible": true, },
                { "targets": [1], "className": "text-left" }
            ],
            "keys": true,
            "keys": { "blurable": false },
            "select": true,
            "select": {
                'style': 'single',
                'selector': 'td:first-child'
            },
            "serverSide": true,
            "processing": true,
            "ajax": function (data, callback, settings)
            {
                var sort_column_name = data.columns[data.order[0].column].data.replace(/\./g, "__");
                var direction = "";
                if (data.order[0].dir == "desc") { direction = "-" };
                $.get("{% static 'colist' %}", {
                    limit: data.length,
                    start: data.start,
                    filter: data.search.value,
                    order_by: direction + sort_column_name
                }, function (res)
                {
                    callback({
                        recordsTotal: res.length,
                        recordsFiltered: res.length,
                        data: res.objects
                    });
                });
            },
            columns: [
                {
                    "data": "0", "render": function (data, type, row)
                    {
                        return '<td class="selected"><input type="checkbox" id="item_20" value="20"><label for="item_20"><span></span></label></td>'
                    }
                },
                { "data": "1" },
                { "data": "2" },
                { "data": "3" },
                { "data": "4" },
                { "data": "5" },
            ]


        });
        table_meters.column(0).visible(false);
    }
    Load_serials_table();


    $('#table_meters tbody').on('click', 'tr', function ()
    {
        if ($(this).hasClass('selected'))
        {
            $(this).removeClass('selected');
        }
        else
        {
            table_meters.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });



};

// Load_serials_table();

function meters_delete(id)
{
    var ok = confirm('Are you sure to delete this entry?');
    if (ok == true)
    {
        $.ajax({
            url: "",
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            contentType: false,
            data: { id: id, },
            success: function (data)
            {
                if (data == 'deleted')
                    table_meters.draw();
            },
            error: function (e)
            {
                alert('err: meter list 158');
            }
        });
    }
}

function meters_assign()
{
    var id = table_meters.rows('.selected').data()[0][0];
    var name = table_meters.rows('.selected').data()[0][1];
    var address = table_meters.rows('.selected').data()[0][2];

    var redirectWindow = window.open("add/", '_blank');
    redirectWindow.location;

    // $('#modal-assign').modal('show').draggable({handle: ".modal-header" });

    // $.ajax({
    //     url: "",
    //     type: 'GET',
    //     dataType: 'json',
    //     contentType: 'application/json; charset=utf-8',
    //     contentType: false,
    //     data: { id:id, name: name, },
    //     success: function (data)
    //     {
    //         window.open("add/", '_blank');
    //     },
    //     error: function (e)
    //     {
    //         alert('err: meter list 158');
    //     }
    // });

}



