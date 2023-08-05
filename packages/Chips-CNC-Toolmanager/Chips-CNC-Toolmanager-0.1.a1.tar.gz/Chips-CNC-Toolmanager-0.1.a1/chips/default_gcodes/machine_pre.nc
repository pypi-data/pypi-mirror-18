(Machine: {{machine_name}})
(Tool: No. {{tool_number}}, {{tool_name}}, {{tool_diameter}}mm)
G21
G90
G94
G0 Z{{machine_safe_z}}
M3 S{{test_startS}}
G4 P5

