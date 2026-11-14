`````
[
  {
    "mr_id": "MR1",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint. For UPWARD_RA, make Own_Tracked_Alt slightly lower than Other_Tracked_Alt; for DOWNWARD_RA, make Own_Tracked_Alt slightly higher; for UNRESOLVED, set them equal to their midpoint. All other inputs remain unchanged.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR2",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify Up_Separation and Down_Separation according to the source output. For UPWARD_RA, decrease Down_Separation. For DOWNWARD_RA, increase Up_Separation and adjust Down_Separation according to Climb_Inhibi. For UNRESOLVED, decrease Up_Separation and increase Down_Separation while preserving the corresponding separation condition. All other inputs remain unchanged.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR3",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify Alt_Layer_Value by one level within its valid range. For UPWARD_RA, increase Alt_Layer_Value by 1; for DOWNWARD_RA, decrease it by 1; for UNRESOLVED, decrease it when Own_Tracked_Alt is not greater than Other_Tracked_Alt, otherwise increase it. All other inputs remain unchanged.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR4",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify both the relative aircraft altitudes and vertical separation values. Adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the relative altitude configuration associated with the source output, and simultaneously modify Up_Separation and/or Down_Separation so that the corresponding separation condition remains satisfied, considering Climb_Inhibi when applicable.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR5",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify both the relative aircraft altitudes and Alt_Layer_Value. Adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the relative altitude configuration associated with the source output, and change Alt_Layer_Value by one valid level in the direction determined by the source output and altitude relationship.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR6",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify both vertical separation values and the relative aircraft altitudes. Adjust Up_Separation and/or Down_Separation to preserve the separation condition associated with the source output, considering Climb_Inhibi when applicable, and adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the corresponding relative altitude configuration.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR7",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify both Alt_Layer_Value and the relative aircraft altitudes. Change Alt_Layer_Value by one valid level according to the source output and current altitude relationship, and adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the corresponding relative altitude configuration.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR8",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify both vertical separation values and Alt_Layer_Value. Adjust Up_Separation and/or Down_Separation to preserve the separation condition associated with the source output, considering Climb_Inhibi when applicable, and change Alt_Layer_Value by one valid level according to the source output and altitude relationship.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR9",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": "Modify both Alt_Layer_Value and the vertical separation values. Change Alt_Layer_Value by one valid level according to the source output and altitude relationship, and adjust Up_Separation and/or Down_Separation so that the corresponding separation condition remains satisfied, considering Climb_Inhibi when applicable.",
    "output_relation": "The follow-up output should be identical to the source output.",
    "actual_relation_status": "SMG"
  }
]
{
"mr_id": "MR1",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint. For UPWARD_RA, make Own_Tracked_Alt slightly lower than Other_Tracked_Alt; for DOWNWARD_RA, make Own_Tracked_Alt slightly higher; for UNRESOLVED, set them equal to their midpoint. All other inputs remain unchanged.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR2",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify Up_Separation and Down_Separation according to the source output. For UPWARD_RA, decrease Down_Separation. For DOWNWARD_RA, increase Up_Separation and adjust Down_Separation according to Climb_Inhibi. For UNRESOLVED, decrease Up_Separation and increase Down_Separation while preserving the corresponding separation condition. All other inputs remain unchanged.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR3",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify Alt_Layer_Value by one level within its valid range. For UPWARD_RA, increase Alt_Layer_Value by 1; for DOWNWARD_RA, decrease it by 1; for UNRESOLVED, decrease it when Own_Tracked_Alt is not greater than Other_Tracked_Alt, otherwise increase it. All other inputs remain unchanged.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR4",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify both the relative aircraft altitudes and vertical separation values. Adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the relative altitude configuration associated with the source output, and simultaneously modify Up_Separation and/or Down_Separation so that the corresponding separation condition remains satisfied, considering Climb_Inhibi when applicable.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR5",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify both the relative aircraft altitudes and Alt_Layer_Value. Adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the relative altitude configuration associated with the source output, and change Alt_Layer_Value by one valid level in the direction determined by the source output and altitude relationship.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR6",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify both vertical separation values and the relative aircraft altitudes. Adjust Up_Separation and/or Down_Separation to preserve the separation condition associated with the source output, considering Climb_Inhibi when applicable, and adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the corresponding relative altitude configuration.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR7",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify both Alt_Layer_Value and the relative aircraft altitudes. Change Alt_Layer_Value by one valid level according to the source output and current altitude relationship, and adjust Own_Tracked_Alt and Other_Tracked_Alt toward their midpoint while preserving the corresponding relative altitude configuration.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR8",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify both vertical separation values and Alt_Layer_Value. Adjust Up_Separation and/or Down_Separation to preserve the separation condition associated with the source output, considering Climb_Inhibi when applicable, and change Alt_Layer_Value by one valid level according to the source output and altitude relationship.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
},
{
"mr_id": "MR9",
"source_test_id": "",
"followup_test_id": "",
"input_transformation": "Modify both Alt_Layer_Value and the vertical separation values. Change Alt_Layer_Value by one valid level according to the source output and altitude relationship, and adjust Up_Separation and/or Down_Separation so that the corresponding separation condition remains satisfied, considering Climb_Inhibi when applicable.",
"output_relation": "The follow-up output should be identical to the source output.",
"actual_relation_status": "SMG"
}
]  TRANSLATION 
MR1‑MR9 JSON  Chinese Translation of Fields 
 A few words about terms 
Own_Tracked_Alt : own aircraft Tracking Altitude 
Other_Tracked_Alt : intruder aircraft Tracking Altitude 
Up_Separation : Upward safety margin 
Down_Separation : Downward safety margin 
Alt_Layer_Value : altitude layer index 
Climb_Inhibi : Climb Inhibition Switch 
source_test_id : Source Test Case Number 
followup_test_id : follow-up test case Number 
input_transformation : input transformation rule 
output_relation : Output metamorphic relation 
actual_relation_status : Actual Relationship Status ( SMG  PENDING 
json
[
  {
    "mr_id": "MR1",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Adjust the own aircraft’s tracking altitude and the intruder aircraft’s tracking altitude to near the midpoint between the two. If the original output is UPWARD_RA , so that the tracking altitude of this aircraft is slightly lower than the tracking altitude of the intruder aircraft; if DOWNWARD_RA , so that the tracking altitude of this aircraft is slightly higher than the tracking altitude of the intruder aircraft; if UNRESOLVED , set both to the midpoint value. All other inputs remain unchanged. ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR2",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Modify the upper safety margin and the lower safety margin based on the source program output. The output is UPWARD_RA When , reduce the downward safety margin; the output is DOWNWARD_RA Increase the upward safety margin and adjust the downward safety margin according to the climb inhibition switch; the output is UNRESOLVED When , reduce the upward safety margin and increase the downward safety margin while maintaining the corresponding margin constraints. All other inputs remain unchanged. ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR3",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Apply ± to the altitude layer index within the valid range of values 1 Adjustment. Output is UPWARD_RA , altitude layer index Plus 1 ; Output is DOWNWARD_RA , altitude layer index Decrease 1 ; Output is UNRESOLVED , the index decreases when the own aircraft’s tracking altitude is not higher than the intruder’s tracking altitude 1 , otherwise, the index is incremented 1 . All other inputs remain unchanged. ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR4",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Simultaneously modify the relative altitude and vertical separation of the two aircraft. Adjust the tracking altitudes of this aircraft and the intruder aircraft to near the midpoint between the two, maintaining the relative altitude relationship corresponding to the source output; simultaneously modify the upward / For the downward safety margin, ensure that the corresponding margin constraints are met, and consider the climb inhibition switch if necessary. ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR5",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Simultaneously modify the relative altitudes of the two aircraft and the altitude level index. Adjust the tracking altitudes of this aircraft and the intruder aircraft to near the midpoint between the two, maintaining the relative altitude relationship corresponding to the source output; then, based on the relationship between the source output and the altitudes of the two aircraft, adjust the altitude layer index by ± within the valid range. 1 ”Do so.” ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR6",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Simultaneously modify the vertical separation and the relative altitude of the two aircraft. Adjust upwards first. / Maintain the separation constraint corresponding to the source output for the downward safety separation, and consider the climb inhibition switch if necessary; then adjust the tracking altitudes of the own aircraft and the intruder aircraft to near the midpoint between the two, maintaining the corresponding relative altitude relationship. ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR7",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Simultaneously modify the altitude layer index and the relative altitude between the two aircraft. Based on the relationship between the source output and the current altitude, adjust the altitude level index by ± within the valid range. 1 Adjust; then adjust the tracking altitude of this aircraft and the intruder aircraft to near the midpoint between the two, maintaining the corresponding relative altitude relationship. ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR8",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Simultaneously modify the vertical separation and altitude layer index. Adjust upwards. / For the lower safety margin, maintain the margin constraint corresponding to the source output, and consider the climb inhibition switch if necessary; then, based on the relationship between the source output and the altitudes of the two aircraft, adjust the altitude level index within the valid range by ± 1 ”Do so.” ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  },
  {
    "mr_id": "MR9",
    "source_test_id": "",
    "followup_test_id": "",
    "input_transformation": " Simultaneously modify the altitude layer index and the vertical separation. Based on the relationship between the source output and the altitudes of the two aircraft, adjust the altitude layer index by ± within the valid range. 1 Adjustment; readjustment upwards / For the downward safety margin, ensure that the corresponding margin constraints are met, and consider the climb inhibition switch if necessary. ",
    "output_relation": " The output of the derived use case should be consistent with the output of the source use case. ",
    "actual_relation_status": "SMG"
  }
]
 Field Definition Table 
 Table Filter 
 English field 	 Chinese meaning 
mr_id	 metamorphic relation ID 
source_test_id	 Source Test Case  ID
followup_test_id	 follow-up test case  ID
input_transformation	 input transformation rule 
output_relation	 Output metamorphic relation Specification 
actual_relation_status	 Actual relationship status, SMG =  Pending Evaluation 
 Definition in Business  output_relation : metamorphic relation expectation: The output of the follow-up input should be equal to the output of the original input. 
 In the code: result=0  Satisfy the relationship; result=1 Violation of result=2 This use case is for  MR  invalid.  
 If you need it, I can put this...  9  organized into the paper  markdown  Table Filter 



`````

