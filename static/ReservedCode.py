#        # key = call_key()
#         # a = Fernet(key)
#         # name = a.encrypt(str.encode())
#         # print('name', request.GET.get('name'))
#         # coded_slogan = a.encrypt(slogan)
#         # print(coded_slogan)

# #        // function meter_to_datatable(params)
# # // {
# #     // if ($('#id_serialnos').val() == '')
# #     // {
# #         // $('#id_serialnos').focus()
# #         // return
# #         //}
# #     // if ($('#id_units').val() == '')
# #     // {
# #         // $('#id_units').focus()
# #         // return
# #         //}
# #     // tablex.row.add([
# #         // 0,
# #         // $("#id_brandid option:selected").text(),
# #         // $("#id_mtypeid option:selected").text(),
# #         // $('#id_units').val(),
# #         // $('#id_serialnos').val(),
# #         // $('#id_brandid').val(),
# #         // $('#id_mtypeid').val(),
# #         // ]).draw(false)
# #     // }


# # // $(".id_brandid").select2().val(1).trigger('change.select2')
# # // $(".id_mtypeid").select2().val(1).trigger('change.select2')


# window.onload = function()
# {
#     function loadMeters()
#     {
#         table = $('#table_meters').DataTable({
#             "scrollX": true,
#             "searching": false,
#             "info": false,
#             "lengthChange": true,
#             "keys": true,
#             "keys": {"blurable": false},
#             "columnDefs": [
#                 {"targets": [0], "searchable": false, "orderable": false, "visible": true}, // "className": "select-checkbox icheck-primary",
#                 // {"targets": [1], "visible": false},
#                 // {"targets": [6], "className": "text-left"}
#             ],
#             "select": true,
#             "select": {
#                 "style": 'multi',
#                 "selector": 'td:first-child',
#             },
#             "serverSide": true,
#             "processing": true,
#             "ajax": function(data, callback, settings)
#             {
#                 var sort_column_name = data.columns[data.order[0].column].data.replace( /\./g, "__")
#                 var direction=""
#                 if (data.order[0].dir == "desc") {direction="-"}
#                 $.get(meterlUrl, {
#                     limit: data.length,
#                     start: data.start,
#                     filter: data.search.value,
#                     order_by: direction + sort_column_name
#                 }, function(res)
#                     {
#                     callback({
#                         recordsTotal: res.length,
#                         recordsFiltered: res.length,
#                         data: res.objects
#                     })
#                 })
#             },
#             columns: [
#                 {
#                     "data": "id", "render": function(data, type, row)
#                     {
#                         return '<td class="selected"><input type="checkbox" id="item_20" value="20"><label for="item_20"><span></span></label></td>'
#                     }
#                 },
#                 {
#                     "data": "id", "render": function(data, type, row)
#                     {
#                         if (data == 2)
#                         {
#                             return '<span style="font-size: 12px;" title="Returned to warehouse"> Returned</span></a>'
#                         } else
#                         {
#                             if (row["status"] >= 1)
#                             {
#                                 return '<a href="calibrate/' + row["id"] + '" class="btn btn-default btn-xs text-xs" title="Calibrate"> <span style = "font-size: 12px;"> Calibrated</span ></a>'
#                             } else
#                             {
#                                 return '<a href="calibrate/' + row["id"] + '" class="btn btn-info btn-xs text-xs" title="Calibrate"> <span style = "font-size: 12px;"> Calibrate</span ></a>'
#                             }
#                         }
#                     }
#                 },
#                 {
#                     "data": "status", "render": function(data, type, row)
#                     {
#                         if (data == 1)
#                         {
#                             return '<span style="color: rgb(79, 139, 18);"> Passed</span>'
#                         } else if (data == 2)
#                         {
#                             return '<span style="color: rgb(255, 0, 0);">Failed</span>'
#                         } else
#                         {
#                             return '<span>Pending</span>'
#                         }
#                     }
#                 },
#                 {
#                     "data": "serialno", "render": function(data, type, row)
#                     {
#                         return '<td style="width: fit-content;">' + data + '</td>'
#                     }
#                 },
#                 {
#                     "data": "accuracy", "render": function(data, type, row)
#                     {
#                         if (data == "None")
#                         {
#                         } else
#                         {
#                             return data
#                         }
#                     }
#                 },

#             ],
#             "fnInitComplete": function(oSettings, json)
#             {$('#table_meters tbody tr:eq(0)').click()
#              },
#         })
#     }
#     loadMeters()
#     // table.columns.adjust().draw()

#     $('#table_meterdetails tbody').on('click', 'tr', function()
#                                       {
#         if ($(this).hasClass('selected'))
#         {$(this).removeClass('selected')
#          }
#         else
#         {
#             table.$('tr.selected').removeClass('selected')
#             $(this).addClass('selected')
#         }

#         var data=table.rows(this).data()
#         var id=data[0]['id']
#         var idmeters=data[0]['idmeters']
#         var serials=data[0]['serialno']
#         change_table3_data(id, serials, idmeters)
#     })

#     $(window).bind('resize', function()
#                    {$('#table_meterdetails').css('width', '100%')
#                     $('#table3').css('width', '100%')
#                     })

#     $('#select_all').on('click', function()
#                         {
#         var rows=table.rows({'search': 'applied'}).nodes()
#         $('input[type="checkbox"]', rows).prop('checked', this.checked)
#     })

#     function change_table3_data(id=0, serials=0, idmeters=0)
#     {$.ajax({
#         url: mSelectedUrl,
#         method: 'GET',
#         type: 'GET',
#         data: {
#                 id: id,
#                 serials: serials,
#                 idmeters: idmeters
#         },
#         success: function(data)
#         {$("#meter-history").html(data)
#          $('#id_serial').html(serials)
#          $('#idmeterserials').val(id)
#          },
#         error: function(e)
#         {
#             alert('err: meterdetails.html-202')
#         }
#     })
#     } change_table3_data(id, 0)
# }

# // function return_selectedTable() {
#     // var itemcode, qty
#     // var count = table.rows('.selected').count()
#     // if (count <= 0) return
#     // var ok = confirm('Are you sure to return selected row(s) to warehouse?')
#     // if (ok == true) {
#         // data = table.rows('.selected').data()
#         // data.each(function(value, index) {
#             // if (value['status'] == "None" | | value['status'] == null) {
#                 // alert('Meter ' + value['serialno'] + " is not yet calibrated!")
#                 //} else {
#                 // save_return_selectedTable(value['id'], value['serialno'])
#                 //}
#             //})
#         //}
#     //}

# // function save_return_selectedTable(id=0, serialno='') {
#     // $.ajax({
#         // url: "",
#         // method: 'GET',
#         // type: 'GET',
#         // data: {id: id, },
#         // success: function(data) {
#               // $.ajax({
#                   // success: function(data) {
#                         // table.ajax.reload(null, false)
#                         // msgalert("Returned", "Meter [" + serialno + "] successfully returned to warehouse", 1)
#                         // },
#                   // error: function() {
#                       // alert('Err: save_return_selectedTable')
#                       //}
#                   //})
#               //},
#         //})
#     //}
