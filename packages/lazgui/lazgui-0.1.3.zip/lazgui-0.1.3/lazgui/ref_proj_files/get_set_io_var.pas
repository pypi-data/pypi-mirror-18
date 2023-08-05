unit get_set_io_var;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils,   Forms, Controls, Graphics,
  Buttons, Variants,   Dialogs, ExtCtrls,
  typinfo;

function GetIOVarText(Control: TControl):String;
procedure SetIOVarText(Control: TControl; new_text:String);

function GetIOVarString(Control: TControl; def_val:String; const lab:string):String;
function GetIOVarInteger(Control: TControl; def_val:Integer; const lab:string):Integer;
function GetIOVarDouble(Control: TControl; def_val:Double; const lab:string):Double;
function GetIOVarBoolean(Control: TControl; def_val:Boolean; const lab:string):Boolean;


implementation

function GetIOVarText(Control: TControl):String;
// Get text property
var
  PropInfo  : PPropInfo;
  //Items : TStringList;
  i : integer;
begin

  Result := '';
  
  PropInfo := GetPropInfo(Control, 'Text');
  if PropInfo<>nil then
      begin
        Result := GetPropValue(Control, 'Text');
        exit;
      end;


  PropInfo := GetPropInfo(Control, 'ItemIndex');
  if PropInfo<>nil then
      begin
        i := GetPropValue(Control, 'ItemIndex');
        PropInfo := GetPropInfo(Control, 'Items');

        if PropInfo<>nil then
            begin
                 //Items := GetObjectProp(Control, 'Items') As TStringList;
                 Result := (GetObjectProp(Control, 'Items') As TStringList)[i]
            end;
      end;

end;                

procedure SetIOVarText(Control: TControl; new_text:String);
// Set text property
var
  PropInfo  : PPropInfo;
  i : integer;
begin
  PropInfo := GetPropInfo(Control, 'Text');
  if PropInfo<>nil then
      begin
        SetPropValue(Control, 'Text', new_text);
      end;

  PropInfo := GetPropInfo(Control, 'ItemIndex');
  if PropInfo<>nil then
      begin

          i := (GetObjectProp(Control, 'Items') As TStringList).IndexOf(new_text);
          //ShowMessage('i = '+IntToStr(i));
          if (i >= 0) then
            SetPropValue(Control, 'ItemIndex', i);
      end
end;
// ===================================

function GetIOVarString(Control: TControl; def_val:String; const lab:string):String;
begin
  try
     Result := VarAsType(GetIOVarText(Control), varString);
  except
     ShowMessage( 'Error in "' + lab + '" Int Value = "' + GetIOVarText(Control) + '".' + #13
                  + ' Using "' + def_val + '" instead.' );
     Result := def_val;
  end;
end;
  
// ===================================
function GetIOVarInteger(Control: TControl; def_val:Integer; const lab:string):Integer;
begin
  try
     Result := VarAsType(GetIOVarText(Control), varInteger);
  except
     ShowMessage( 'Error in "' + lab + '" Int Value = "' + GetIOVarText(Control) + '".' + #13
                  + ' Using "' + IntToStr(def_val) + '" instead.' );
     Result := def_val;
  end;
end;

// ===================================
  
function GetIOVarDouble(Control: TControl; def_val:Double; const lab:string):Double;
begin
  try
    Result := VarAsType(GetIOVarText(Control), varDouble);
  except
     ShowMessage( 'Error in "' + lab + '" Int Value = "' + GetIOVarText(Control) + '".' + #13
                  + ' Using "' + FloatToStr(def_val) + '" instead.' );
     Result := def_val;
  end;
end;
  
// ===================================
function GetIOVarBoolean(Control: TControl; def_val:Boolean; const lab:string):Boolean;
begin
  try
     Result := VarAsType(GetIOVarText(Control), varBoolean);
  except
     ShowMessage( 'Error in "' + lab + '" Int Value = "' + GetIOVarText(Control) + '".' + #13
                  + ' Using "' + BoolToStr(def_val) + '" instead.' );
     Result := def_val;
  end;
end;
  
end.

