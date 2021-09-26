window.onload = function ()
{

    function loadAcquisition()
    {
        acqTable = $('#acqTable').DataTable({
            "searching": false,
            "processing": true,
            "stateSave": true,
            "info": false,
            "paging": true,
            "lengthChange": true,
            "autoWidth": false,
            "responsive": true,
            "columnDefs": [
                { "targets": [0], "searchable": false, "orderable": false, "visible": true },
                // { "targets": [5], "className": "text-left" }
            ],
            "keys": true,
            "keys": { "blurable": false },
            "select": true,
            "select": {
                "style": 'multi',
                "selector": 'td:first-child',
            },
            "serverSide": true,
            "processing": true,
            "ajax": function (data, callback, settings)
            {
                var sort_column_name = data.columns[data.order[0].column].data.replace(/\./g, "__");
                var direction = "";
                if (data.order[0].dir == "desc") { direction = "-" };
                $.get(acqListUrl, {
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
                    "data": "id", "render": function (data, type, row)
                    {
                        return '<td class="selected"><input type="checkbox" id="item_20" value="20"><label for="item_20"><span></span></label></td>'
                    }
                },
                {
                    "data": "id", "render": function (data, type, row)
                    {
                        if ('{{ request.user.is_superuser }}' == 'True')
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="#" class="btn btn-warning btn-xs text-sm" title="Edit" onclick = "" ><i class="fas fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick = "meter_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                        else
                        {
                            return '<center>' +
                                '<div class="btn-group">' +
                                '<a href="edit/' + row["id"] + '" class="btn btn-warning btn-xs text-sm" title="Edit"><i class="fal fa-pencil-alt"></i><span style="font-size: 12px;"> Edit</span></a>' +
                                '<a href="#" class="btn btn-danger btn-xs text-sm" title="Delete" onclick = "meter_delete(' + row["id"] + ')" ><i class="fal fa-trash-alt"></i><span style="font-size: 12px;"></span></a>' +
                                '</div>' +
                                '</center>'
                        }
                    }
                },
                {
                    "data": "transactiondate", "render": function (data, type, row)
                    {
                        return '<td style="width: fit-content;"> <a href="details/' + row["id"] + '">' + data + '</a></td>'
                    }
                },
                { "data": "supplierid__suppliername" },
                { "data": "supplierid__address" },
            ]
        });
        acqTable.column(0).visible(false);
    }
    loadAcquisition();

    // $('#acqTable tbody').on('click', 'tr', function ()
    // {
    //     if ($(this).hasClass('selected'))
    //     {
    //         $(this).removeClass('selected');
    //     }
    //     else
    //     {
    //         acqTable.$('tr.selected').removeClass('selected');
    //         $(this).addClass('selected');
    //     }

    //     var data = acqTable.rows(this).data();
    //     var id = data[0]['id'];
    //     show_details(id );
    // });

    // function show_details(id)
    // {
    //     $.ajax({
    //         url: acqSelectedUrl,
    //         method: 'GET',
    //         type: 'GET',
    //         data: { id: id,
    //         },
    //         success: function (data)
    //         {
    //             $("#metersdata").html(data);
    //         },
    //         error: function (e)
    //         {
    //             alert('err: meters.js - show_details');
    //         }
    //     });
    // } change_table3_data(id, 0);

};

// function modal_acquisition(params)
// {
//     $('#modal-acquisition').modal('show').draggable({ handle: ".modal-header" });
// }


// function meter_save(id)
// {
//     $.ajax({
//         url: mDelete.replace('0', id),
//         type: 'GET',
//         dataType: 'json',
//         contentType: 'application/json; charset=utf-8',
//         contentType: false,
//         data: { id: id, },
//         success: function (data)
//         {

//         },
//         error: function (e)
//         {
//             alert('err: meter list 158');
//         }
//     });
// }

function meter_delete(id)
{
    var ok = confirm('Are you sure to delete this entry?');
    if (ok == true)
    {
        $.ajax({
            url: mDelete.replace('0', id),
            type: 'GET',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            contentType: false,
            data: { id: id, },
            success: function (data)
            {
                if (data == 'deleted')
                    acqTable.draw();
            },
            error: function (e)
            {
                alert('err: meter list 158');
            }
        });
    }
}