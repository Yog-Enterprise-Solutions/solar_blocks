frappe.ui.form.on('Task', {
	project_status:function(frm) {
		if (frm.doc.project_status==='Completed'){frm.doc.completed_by=frappe.session.user}
	},
    refresh: function(frm) {
        setTimeout(() => {
	        $('.form-link-title').hide();
	        $('.form-sidebar-stats').hide();
	        $('.sidebar-image-wrapper').hide();
            $("[data-label='Create']").hide();
            $("[data-label='Connections']").hide();
	        $('.indicator-pill').hide()
	        $('.comment-box').hide();
	        $('.comment-box').hide();
	        $('.row.form-dashboard-section.form-links').hide();
	       
 

	        $("[data-doctype='Timesheet']").hide();
	        
	        

        }, 10);
        frm.set_df_property('welcome_call','hidden',1)
        frm.set_df_property('site_assessment','hidden',1)
        frm.set_df_property('engineering','hidden',1)
        frm.set_df_property('permitting','hidden',1)
        frm.set_df_property('installation','hidden',1)
        frm.set_df_property('closeout','hidden',1)
        
        if(frm.doc.subject=="WELCOME CALL" || frm.doc.subject=="Welcome Call" || frm.doc.subject=="Welcome call" || frm.doc.subject=="welcome call"){
            frm.set_df_property('welcome_call','hidden',0)
            
            // if(frm.doc.briefed_about_contract_add_ons_=="1"){
            //     frm.set_df_property('briefed_about_contract_add_ons_','read_only',1)
            //     frm.set_df_property('all_documents_collected_','read_only',0)
            // }else{
            //     frm.set_df_property('all_documents_collected_','read_only',1)
            // }
            // if(frm.doc.all_documents_collected_=="1"){
            //     frm.set_df_property('all_documents_collected_','read_only',1)
            // }
        }
        
        if(frm.doc.subject=="SITE VISIT" || frm.doc.subject=="Site Visit" || frm.doc.subject=="site visit" || frm.doc.subject=="Site visit" || frm.doc.subject=="site Visit" ){
            frm.set_df_property('site_visit','hidden',0)
            // if(frm.doc.schedule_visit_=="1"){
            //     frm.set_df_property('schedule_visit_','read_only',1)
            //     frm.set_df_property('site_visit_completed','read_only',0)
            // }else{
            //     frm.set_df_property('site_visit_completed','read_only',1)
            // }
            // if(frm.doc.site_visit_completed=="1"){
            //     frm.set_df_property('site_visit_completed','read_only',1)
            // }
        }
        
        if(frm.doc.subject=="engineering" || frm.doc.subject=="Engineering" || frm.doc.subject=="ENGINEERING"){
            frm.set_df_property('engineering','hidden',0)
            // if(frm.doc.complete_design_package=="1"){
            //     frm.set_df_property('complete_design_package','read_only',1)
            //     frm.set_df_property('pe_letter','read_only',0)
            // }else{
            //     frm.set_df_property('pe_letter','read_only',1)
            //     frm.set_df_property('bom','read_only',1)
            // }
            // if(frm.doc.pe_letter=="1"){
            //     frm.set_df_property('pe_letter','read_only',1)
            //     frm.set_df_property('bom','read_only',0)
            // }else{
            //     frm.set_df_property('bom','read_only',1)
            // }
            // if(frm.doc.bom=="1"){
            //     frm.set_df_property('bom','read_only',1)
            // }
        }
        
        
        if(frm.doc.subject=="structural permitting" || frm.doc.subject=="Structural Permitting" || frm.doc.subject=="STRUCTURAL PERMITTING"){
            frm.set_df_property('structural_permitting','hidden',0)
            // if(frm.doc.submitted_for_ic=="1"){
            //     frm.set_df_property('submitted_for_ic','read_only',1)
            //     frm.set_df_property('ic_approved_','read_only',0)
            // }else{
            //     frm.set_df_property('submitted_for_permits','read_only',1)
            //     frm.set_df_property('ic_approved_','read_only',1)
            //     frm.set_df_property('permits_approved','read_only',1)
            // }
            // if(frm.doc.ic_approved_=="1"){
            //     frm.set_df_property('ic_approved_','read_only',1)
            //     frm.set_df_property('submitted_for_permits','read_only',0)
            // }else{
            //     frm.set_df_property('submitted_for_permits','read_only',1)
            //     frm.set_df_property('permits_approved','read_only',1)
            // }
            // if(frm.doc.submitted_for_permits=="1"){
            //     frm.set_df_property('submitted_for_permits','read_only',1)
            //     frm.set_df_property('permits_approved','read_only',0)
            // }else{
            //     frm.set_df_property('permits_approved','read_only',1)
            // }
            // if(frm.doc.permits_approved=="1"){
            //     frm.set_df_property('permits_approved','read_only',1)
            // }
        }
        if(frm.doc.subject=="ELECTRICAL PERMIT" || frm.doc.subject=="Electrical Permit" || frm.doc.subject=="electrical permit"){
            frm.set_df_property('structural_permitting','hidden',0)
             
         }
         if(frm.doc.subject=="Pre Install Work" || frm.doc.subject=="pre install work" || frm.doc.subject=="PRE INSTALL WORK"){
            frm.set_df_property('pre_install_work','hidden',0)
             
         }
       
        if(frm.doc.subject=="Final submitted" || frm.doc.subject=="Final Submitted" || frm.doc.subject=="final submitted" || frm.doc.subject=="FINAL SUBMITTED"){
            frm.set_df_property('final_submitted','hidden',0)
             
         }
        if(frm.doc.subject=="ELECTRICAL INSPECTION" || frm.doc.subject=="Electrical Inspection" || frm.doc.subject=="electrical inspection"){
            frm.set_df_property('electrical_inspection','hidden',0)
             
         }
        if(frm.doc.subject=="PTO" || frm.doc.subject=="Pto" || frm.doc.subject=="pto"){
            frm.set_df_property('pto','hidden',0)
             
         }
        if(frm.doc.subject=="Commissioning" || frm.doc.subject=="commissioning" || frm.doc.subject=="COMMISSIONING"){
            frm.set_df_property('commissioning','hidden',0)
             
         } 
         if(frm.doc.subject=="Procurements" || frm.doc.subject=="procurements" || frm.doc.subject=="PROCUREMENTS"){
            frm.set_df_property('procurements','hidden',0)
             
         } 
         if(frm.doc.subject=="Structural Inspection" || frm.doc.subject=="structural inspection" || frm.doc.subject=="STRUCTURAL INSPECTION"){
            frm.set_df_property('structural_inspection','hidden',0)
             
         } 
        
        if(frm.doc.subject=="installation work" || frm.doc.subject=="Installation Work" || frm.doc.subject=="INSTALLATION WORK"){
            frm.set_df_property('installation_work','hidden',0)
            // if(frm.doc.schedule_pre_install_works=="1"){
            //     frm.set_df_property('schedule_pre_install_works','read_only',1)
            //     frm.set_df_property('schedule_installs','read_only',0)
            // }else{
            //     frm.set_df_property('schedule_installs','read_only',1)
            //     frm.set_df_property('order_materialss','read_only',1)
            //     frm.set_df_property('pre_install_work_completeds','read_only',1)
            //     frm.set_df_property('solar_install_started','read_only',1)
            //     frm.set_df_property('solar_install_completed','read_only',1)
            //     frm.set_df_property('install_review_completed','read_only',1)
            // }
            // if(frm.doc.schedule_installs=="1"){
            //     frm.set_df_property('schedule_installs','read_only',1)
            //     frm.set_df_property('order_materialss','read_only',0)
            // }else{
            //     frm.set_df_property('order_materialss','read_only',1)
            //     frm.set_df_property('pre_install_work_completeds','read_only',1)
            //     frm.set_df_property('solar_install_started','read_only',1)
            //     frm.set_df_property('solar_install_completed','read_only',1)
            //     frm.set_df_property('install_review_completed','read_only',1)
            // }
            
            // if(frm.doc.order_materialss=="1"){
            //     frm.set_df_property('order_materialss','read_only',1)
            //     frm.set_df_property('pre_install_work_completeds','read_only',0)
            // }else{
            //     frm.set_df_property('pre_install_work_completeds','read_only',1)
            //     frm.set_df_property('solar_install_started','read_only',1)
            //     frm.set_df_property('solar_install_completed','read_only',1)
            //     frm.set_df_property('install_review_completed','read_only',1)
            // }
            
            // if(frm.doc.pre_install_work_completeds=="1"){
            //     frm.set_df_property('pre_install_work_completeds','read_only',1)
            //     frm.set_df_property('solar_install_started','read_only',0)
            // }else{
            //     frm.set_df_property('solar_install_started','read_only',1)
            //     frm.set_df_property('solar_install_completed','read_only',1)
            //     frm.set_df_property('install_review_completed','read_only',1)
            // }
            
            // if(frm.doc.solar_install_started=="1"){
            //     frm.set_df_property('solar_install_started','read_only',1)
            //     frm.set_df_property('solar_install_completed','read_only',0)
            // }else{
            //     frm.set_df_property('solar_install_completed','read_only',1)
            //     frm.set_df_property('install_review_completed','read_only',1)
            // }
            
            // if(frm.doc.solar_install_completed=="1"){
            //     frm.set_df_property('solar_install_completed','read_only',1)
            //     frm.set_df_property('install_review_completed','read_only',0)
            // }else{
            //     frm.set_df_property('install_review_completed','read_only',1)
            // }
            
            // if(frm.doc.install_review_completed=="1"){
            //     frm.set_df_property('install_review_completed','read_only',1)
            // }
        }

        if(frm.doc.subject=="Interconnection" || frm.doc.subject=="interconnection" || frm.doc.subject=="INTERCONNECTION"){
            frm.set_df_property('interconnection','hidden',0)
            // if(frm.doc.schedule_electrical_inspection=="1"){
            //     frm.set_df_property('schedule_electrical_inspection','read_only',1)
            //     frm.set_df_property('completed_electrical_inspection','read_only',0)
            // }else{
            //     frm.set_df_property('completed_electrical_inspection','read_only',1)
            //     frm.set_df_property('submit_pto','read_only',1)
            //     frm.set_df_property('pto_approved','read_only',1)
            //     frm.set_df_property('submit_final_inspection','read_only',1)
            //     frm.set_df_property('final_inspection_completed','read_only',1)
            //     frm.set_df_property('turn_on_system','read_only',1)
            // }
            // if(frm.doc.completed_electrical_inspection=="1"){
            //     frm.set_df_property('completed_electrical_inspection','read_only',1)
            //     frm.set_df_property('submit_pto','read_only',0)
            // }else{
            //     frm.set_df_property('submit_pto','read_only',1)
            //     frm.set_df_property('pto_approved','read_only',1)
            //     frm.set_df_property('submit_final_inspection','read_only',1)
            //     frm.set_df_property('final_inspection_completed','read_only',1)
            //     frm.set_df_property('turn_on_system','read_only',1)
            // }
            
            // if(frm.doc.submit_pto=="1"){
            //     frm.set_df_property('submit_pto','read_only',1)
            //     frm.set_df_property('pto_approved','read_only',0)
            // }else{
            //   frm.set_df_property('pto_approved','read_only',1)
            //     frm.set_df_property('submit_final_inspection','read_only',1)
            //     frm.set_df_property('final_inspection_completed','read_only',1)
            //     frm.set_df_property('turn_on_system','read_only',1)
            // }
            
            // if(frm.doc.pto_approved=="1"){
            //     frm.set_df_property('pto_approved','read_only',1)
            //     frm.set_df_property('submit_final_inspection','read_only',0)
            // }else{
            //     frm.set_df_property('submit_final_inspection','read_only',1)
            //     frm.set_df_property('final_inspection_completed','read_only',1)
            //     frm.set_df_property('turn_on_system','read_only',1)
            // }
            
            // if(frm.doc.submit_final_inspection=="1"){
            //     frm.set_df_property('submit_final_inspection','read_only',1)
            //     frm.set_df_property('final_inspection_completed','read_only',0)
            // }else{
            //     frm.set_df_property('final_inspection_completed','read_only',1)
            //     frm.set_df_property('turn_on_system','read_only',1)
            // }
            
            // if(frm.doc.final_inspection_completed=="1"){
            //     frm.set_df_property('final_inspection_completed','read_only',1)
            //     frm.set_df_property('turn_on_system','read_only',0)
            // }else{
            //     frm.set_df_property('turn_on_system','read_only',1)
            // }
            
            // if(frm.doc.turn_on_system=="1"){
            //     frm.set_df_property('turn_on_system','read_only',1)
            // }
        }

//         if (frm.doc.task_priority>1){
//             var prev_task = frm.doc.task_priority - 1
//             frappe.call({
//                 method: 'check_task_priority',
//                 args: {
//                   project: frm.doc.project,
//                   prev_task: prev_task
//                 },
//                 callback: function(r) {
//                     console.log(r)
//                     if (r.message === 'Completed') {
//                         frm.toggle_enable('schedule_pre_install_works', 1);
//                         frm.toggle_enable('status', 1);
//                         frm.toggle_enable('subject', 1);
//                         frm.toggle_enable('project', 1);
//                         frm.toggle_enable('issue', 1);
//                         frm.toggle_enable('type', 1);
//                         frm.toggle_enable('color', 1);
//                         frm.toggle_enable('is_group', 1);
//                         frm.toggle_enable('is_template', 1);
//                         frm.toggle_enable('task_priority', 1);
//                         frm.toggle_enable('task_weight', 1);
//                         frm.toggle_enable('parent_task', 1);
//                         frm.toggle_enable('completed_by', 1);
//                         frm.toggle_enable('completed_on', 1);
//                         frm.toggle_enable('exp_start_date', 1);
//                         frm.toggle_enable('expected_time', 1);
//                         frm.toggle_enable('start', 1);
//                         frm.toggle_enable('exp_end_date', 1);
//                         frm.toggle_enable('progress', 1);
//                         frm.toggle_enable('duration', 1);
//                         frm.toggle_enable('is_milestone', 1);
//                         frm.toggle_enable('description', 1);
//                         frm.toggle_enable('depends_on', 1);
//                         frm.toggle_enable('depends_on_tasks', 1);
//                         frm.toggle_enable('act_start_date', 1);
//                         frm.toggle_enable('actual_time', 1);
//                         frm.toggle_enable('act_end_date', 1);
//                         frm.toggle_enable('department', 1);
//                     } else {
//                         frm.toggle_enable('status', 0);
//                         frm.toggle_enable('subject', 0);
//                         frm.toggle_enable('project', 0);
//                         frm.toggle_enable('issue', 0);
//                         frm.toggle_enable('type', 0);
//                         frm.toggle_enable('color', 0);
//                         frm.toggle_enable('is_group', 0);
//                         frm.toggle_enable('is_template', 0);
//                         frm.toggle_enable('task_priority', 0);
//                         frm.toggle_enable('task_weight', 0);
//                         frm.toggle_enable('parent_task', 0);
//                         frm.toggle_enable('completed_by', 0);
//                         frm.toggle_enable('completed_on', 0);
//                         frm.toggle_enable('exp_start_date', 0);
//                         frm.toggle_enable('expected_time', 0);
//                         frm.toggle_enable('start', 0);
//                         frm.toggle_enable('exp_end_date', 0);
//                         frm.toggle_enable('progress', 0);
//                         frm.toggle_enable('duration', 0);
//                         frm.toggle_enable('is_milestone', 0);
//                         frm.toggle_enable('description', 0);
//                         frm.toggle_enable('depends_on', 0);
//                         frm.toggle_enable('depends_on_tasks', 0);
//                         frm.toggle_enable('act_start_date', 0);
//                         frm.toggle_enable('actual_time', 0);
//                         frm.toggle_enable('act_end_date', 0);
//                         frm.toggle_enable('department', 0);
                        
//                         frm.set_df_property('welcome_call','hidden',1)
//                         frm.set_df_property('site_assessment','hidden',1)
//                         frm.set_df_property('engineering','hidden',1)
//                         frm.set_df_property('permitting','hidden',1)
//                         frm.set_df_property('installation','hidden',1)
//                         frm.set_df_property('closeout','hidden',1)
                        
//                     }
//                 }
//             })
      
//         }
    
  },
    validate(frm){
        if(!frm.doc.started_on && !frm.doc.expected_close_date){
            frappe.validated=false;
            frappe.throw('Complete Previous Tasks !');
        }
       
        if(frm.doc.project_status=="Completed"){
            if(frm.doc.subject=="WELCOME CALL" || frm.doc.subject=="Welcome Call" || frm.doc.subject=="Welcome call" || frm.doc.subject=="welcome call"){
                if(frm.doc.all_documents_collected_=="0" || frm.doc.briefed_about_contract_add_ons_=="0"){
                    frappe.msgprint("All Sub Task is not completed")
                    frappe.validated = false;
                }
            }
            if(frm.doc.subject=="SITE ASSESSMENT" || frm.doc.subject=="Site Assessment" || frm.doc.subject=="Site Assesment" || frm.doc.subject=="Site assesment" || frm.doc.subject=="site assesment" ){
                if(frm.doc.site_visit_completed=="0" || frm.doc.schedule_visit_=="0"){
                    frappe.msgprint("All Sub Task is not completed")
                    frappe.validated = false;
                }
            }
            if(frm.doc.subject=="engineering" || frm.doc.subject=="Engineering" || frm.doc.subject=="ENGINEERING"){
                if(frm.doc.complete_design_package=="0" || frm.doc.pe_letter=="0" || frm.doc.bom=="0"){
                    frappe.msgprint("All Sub Task is not completed")
                    frappe.validated = false;
                }
            }
            if(frm.doc.subject=="permitting" || frm.doc.subject=="Permitting" || frm.doc.subject=="PERMITTING"){
                if(frm.doc.submitted_for_ic=="0" || frm.doc.ic_approved_=="0" || frm.doc.submitted_for_permits=="0" || frm.doc.permits_approved=="0"){
                    frappe.msgprint("All Sub Task is not completed")
                    frappe.validated = false;
                }
            }
            if(frm.doc.subject=="installation" || frm.doc.subject=="Installation" || frm.doc.subject=="INSTALLATION"){
                if(frm.doc.schedule_pre_install_works=="0" || frm.doc.schedule_installs=="0" || frm.doc.order_materialss=="0" || frm.doc.pre_install_work_completeds=="0" || frm.doc.solar_install_started=="0" || frm.doc.solar_install_completed=="0" || frm.doc.install_review_completed=="0"){
                    frappe.msgprint("All Sub Task is not completed")
                    frappe.validated = false;
                }
            }
            if(frm.doc.subject=="CLOSEOUT" || frm.doc.subject=="closeout" || frm.doc.subject=="Closeout" || frm.doc.subject=="CloseOut" || frm.doc.subject=="CLOSE OUT"){
                if(frm.doc.schedule_electrical_inspection=="0" || frm.doc.completed_electrical_inspection=="0" || frm.doc.submit_pto=="0" || frm.doc.pto_approved=="0" || frm.doc.submit_final_inspection=="0" || frm.doc.final_inspection_completed=="0" || frm.doc.turn_on_system=="0"){
                    frappe.msgprint("All Sub Task is not completed")
                    frappe.validated = false;
                }
            }
        }

  },
    before_save(frm){

        // if(frm.doc.subject=="WELCOME CALL" || frm.doc.subject=="Welcome Call" || frm.doc.subject=="Welcome call" || frm.doc.subject=="welcome call"){
        //     if(frm.doc.started_on && frm.doc.expected_close_date && frm.doc.scheduled_on){}
        //     else{
        //         frm.doc.started_on=  frappe.datetime.get_today();
        //         frm.doc.expected_close_date = frappe.datetime.add_days(frm.doc.started_on, 2);
        //         frm.doc.scheduled_on = frappe.datetime.add_days(frm.doc.started_on, 2);
        //     }
                
        // }
        // if(frm.doc.subject=="Site Visit" || frm.doc.subject=="site visit" || frm.doc.subject=="Site visit" || frm.doc.subject=="site visit"){
        //     if(frm.doc.started_on && frm.doc.expected_close_date && frm.doc.scheduled_on){}
        //     else{
        //         if 
        //         frm.doc.started_on=  frappe.datetime.get_today();
        //         frm.doc.expected_close_date = frappe.datetime.add_days(frm.doc.started_on, 2);
        //         frm.doc.scheduled_on = frappe.datetime.add_days(frm.doc.started_on, 2);
        //     }
            
        // }

      	var today = frappe.datetime.get_today();
      	//welcomecall
        if(frm.doc.all_documents_collected_=="1" && frm.doc.briefed_about_contract_add_ons_=="1" && frm.doc.discuss_any_adds_on=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //sitevisit
        if(frm.doc.site_visit_scheduled=="1" && frm.doc.pre_install_review_completed=="1" && frm.doc.site_visit_completed=="1")
        {
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //Engineering
        if(frm.doc.complete_design_package=="1" && frm.doc.pe_letter=="1" && frm.doc.bom=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //Permit --- electrical and structural
        if(frm.doc.submitted_for_permits=="1" && frm.doc.permits_approved=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //Installationwork
        if(frm.doc.installer_commissioning_performed=="1" && frm.doc.schedule_installs=="1" && frm.doc.solar_install_completed=="1" && frm.doc.install_review_completed=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //PreInstallWork
        if(frm.doc.schedule_pre_install_works=="1" && frm.doc.pre_install_work_completeds=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //Interconnection
        if(frm.doc.submitted_for_interconnection=="1" && frm.doc.interconnection_received=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //Procurments
         if(frm.doc.solar_material_ordered=="1" && frm.doc.electrical_material_ordered_aggrey=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //commisioning
        if(frm.doc.erray_layout_created_as_part_of_commissioning=="1" && frm.doc.barcodes_scanned=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //pto
        if(frm.doc.pto_submitted=="1" && frm.doc.pto_approved=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //electricalInspection
        if(frm.doc.electrical_inspection_scheduled=="1" && frm.doc.electrical_inspection_approved=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //structuralInspection
        if(frm.doc.structural_inspection_scheduled=="1" && frm.doc.structural_inspection_approved=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        //final_submitted
        if(frm.doc.final_signed_off_submitted=="1" && frm.doc.final_off_received=="1"){
            frm.set_value('status',"Completed")
            frm.set_value('project_status',"Completed")
            frm.set_value('completed_on',today)
        }
        
        
        // if(frm.doc.site_visit_completed=="1" && frm.doc.schedule_visit_=="1"){
        //     frm.set_value('status',"Completed")
        //     frm.set_value('project_status',"Completed")
        //     frm.set_value('completed_on',today)
        // }
        
        
        
        // if(frm.doc.schedule_electrical_inspection=="1" && frm.doc.completed_electrical_inspection=="1" && frm.doc.submit_pto=="1" &&frm.doc.pto_approved=="1" && frm.doc.submit_final_inspection=="1" && frm.doc.final_inspection_completed=="1" && frm.doc.turn_on_system=="1"){
        //     frm.set_value('status',"Completed")
        //     frm.set_value('project_status',"Completed")
        //     frm.set_value('completed_on',today)
        // }
        
   },
   
})