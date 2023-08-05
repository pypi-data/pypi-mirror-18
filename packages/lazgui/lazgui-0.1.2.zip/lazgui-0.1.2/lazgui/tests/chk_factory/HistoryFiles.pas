{* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

Author:       Andrea Russo Italy
Description:  THistoryFiles stores the recent files list into an .ini file and
              shows the result into a menu.
              It's possibile to insert the list into any point of your menu.
              A method helps you to have access to all the properties and methods
              of the Menu Items so for example do you can specify the image
              of each item.

EMail:        http://www.andrearusso.it
              info@andrearusso.it

Creation:     January 2005
Modifed:      February 2013 (see Readme.txt)

Version:      1.3.0 For Delphi 2,3,4,5,6,7,8,D2005,D2009,Kylix and Lazarus
              (also all standard and personal editions)

Tested on:    Delphi 2,3,4,6,7,D2005,D2009 all personal or standard editions;
              Kylix 3 Open Edition
              Lazarus

Support:      If do you find a bug, please make a short program which reproduce
              the problem attach it to a message addressed to me.
              If I can reproduce the problem, I can find a fix !
              Do not send exe file but just source code and instructions.
              Always use the latest version (beta if any) before reporting any bug.

Legal issues: Copyright (C) 2005-2013 by Andrea Russo
              info@andrearusso.it
              http://www.andrearusso.it

              This software is provided 'as-it-is', without any express or
              implied warranty. In no event will the author be held liable
              for any damages arising from the use of this software.

              Permission is granted to anyone to use this software for any
              purpose, including commercial applications, and to alter it
              and redistribute it freely, subject to the following
              restrictions:

              1. The origin of this software must not be misrepresented,
                 you must not claim that you wrote the original software.
                 If you use this software in a product, an acknowledgment
                 in the product documentation would be appreciated but is
                 not required.

              2. Altered source versions must be plainly marked as such, and
                 must not be misrepresented as being the original software.

              3. This notice may not be removed or altered from any source
                 distribution.

              4. If do you alter this component please send to me the source
                 to following email address: info@andrearusso.it
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *}

unit HistoryFiles;

//Lazarus
{$MODE Delphi}

interface

//Lazarus
  uses IniFiles, Menus, SysUtils, Classes, Dialogs, Forms, LResources,
    LazarusPackageIntf, Graphics, FileUtil;

Const

MsgPositionOutOfRange = 'Position out of range';
MsgParentMenuNotAssigned = 'ParentMenu not assigned';
MsgIndexOutOfRange = 'Index out of range';

Type

TSeparatorStyle = (sepNone, sepTop, sepBottom, sepBoth);

THistoryItemClick = procedure (Sender: TObject; Item: TMenuItem; const Filename: string) of object;
THistoryCreateItem = procedure (Sender: TObject; Item: TMenuItem; const Filename: string) of object;

Items = 1..255;

  THistoryFiles = class(TComponent)
  private
    FItems : TStringList;

    FOnHistoryItemClick : THistoryItemClick;
    FOnHistoryCreateItem : THistoryCreateItem;

    FMaxItems : Items;
    FIniKey : string;
    FLocalPath : string;
    FIniFile : string;
    FParentMenu : TMenuItem;
    FSeparator : TSeparatorStyle;
    FShowFullPath : boolean;
    FPosition : integer;
    FLastItemIndex : integer;
    FNumberOfItems : Integer;
    FCount : Integer;
    FFileMustExist : boolean;
    FOriginalMainMenuItems : Integer;
    FSorted : boolean;
    FShowNumber : boolean;

    FItemBitmap : TBitmap;
    FItemSelectedBitmap : TBitmap;
    FCheckLastItem : boolean;

    procedure ClearMenu(MainMenu: TMenuItem);
    procedure OnMainMenuClickHistoryItem(Sender:TObject);
    procedure SetParentMenu(const Value: TMenuItem);
    procedure SetPosition(const Value: Integer);
    procedure ReadIniSection(var List : TStringList; LocalIniFile : TIniFile; var bChanged : boolean);
    procedure WriteIniSection(const List : TStringList; LocalIniFile : TIniFile);
    procedure InternalUpdateParentMenu(const CurrentList : TStringList);
    procedure ChangeSort(const Sorted : boolean);
    function  GetLastItemIndex: integer;
    procedure SetLastItemIndex(const Index: integer);
    procedure LastItemIndex_WriteIni;
    procedure SetItemBitmap(const b: TBitmap);
    procedure SetItemSelectedBitmap(const b: TBitmap);

  protected
  public
    constructor Create( AOwner : TComponent ); override;
    destructor  Destroy; override;
    procedure   UpdateList(thefile: string);
    procedure   UpdateParentMenu;
    function    GetItemValue(const Index : integer): string;
    procedure   DeleteItem(const Index : integer);

    property  Count : Integer read FCount;
    property  LastItemIndex : Integer read GetLastItemIndex write SetLastItemIndex default 0;

    procedure ClearLastItem;

  published
    property MaxItems : Items read FMaxItems write FMaxItems default 5;
    property IniKey : string read FIniKey write FIniKey;
    property LocalPath : string read FLocalPath write FLocalPath;
    property ShowFullPath : boolean read FShowFullPath write FShowFullPath default True;
    property IniFile : string read FIniFile write FIniFile;
    property ParentMenu : TMenuItem read FParentMenu write SetParentMenu;
    property Separator : TSeparatorStyle read FSeparator write FSeparator default sepNone;
    property Position : Integer read FPosition write SetPosition default 0;
    property FileMustExist : boolean read FFileMustExist write FFileMustExist default False;
    property Sorted : boolean read FSorted write ChangeSort default False;
    property ShowNumber : boolean read FShowNumber write FShowNumber default True;
    property OnClickHistoryItem : THistoryItemClick read FOnHistoryItemClick write FOnHistoryItemClick;
    property OnCreateItem : THistoryCreateItem read FOnHistoryCreateItem write FOnHistoryCreateItem;

    property ItemBitmap : TBitmap read FItemBitmap write SetItemBitmap;
    property ItemSelectedBitmap : TBitmap read FItemSelectedBitmap write SetItemSelectedBitmap;
    property CheckLastItem : boolean read FCheckLastItem write FCheckLastItem default false;
  end;

procedure Register;

implementation

procedure Register;
begin
  RegisterComponents('AR', [THistoryFiles]);
end;

constructor THistoryFiles.Create( AOwner : TComponent );
begin
  inherited Create( AOwner );
  FIniKey:='History Files';
  FMaxItems:=5;
  FLocalPath:='';
  FIniFile:='History.ini';
  FParentMenu:=nil;
  FSeparator:=sepNone;
  FOriginalMainMenuItems:=0;
  FItems := TStringList.Create;
  FShowFullPath:=True;
  FPosition:=0;
  FLastItemIndex :=0;
  FNumberOfItems:=0;
  FCount:=0;
  FOnHistoryItemClick:=nil;
  FOnHistoryCreateItem:=nil;
  FFileMustExist:=False;
  FSorted:=False;
  FShowNumber:=True;
  FItemBitmap := TBitmap.Create;
  FItemSelectedBitmap := TBitmap.Create;
  FCheckLastItem := false;
end;

destructor THistoryFiles.Destroy;
Begin
  Inherited destroy;
  FItems.Free;
  FItemBitmap.Free;
  FItemSelectedBitmap.Free;
end;

function Upper(s : string): string;
begin
{$IfNDef LINUX}
  Result:=UpperCase(s);
{$ELSE}
  Result:=s;
{$EndIf}

end;

procedure THistoryFiles.ChangeSort(const Sorted : boolean);
var
  List : TStringList;
  LocalIniFile : TIniFile;
  bChanged : boolean;
  sLastFile : string;
begin

  if (csDesigning in ComponentState) and not(csLoading in ComponentState) then
    FSorted := Sorted
  else
    begin
      bChanged := false;

      if FSorted <> Sorted then
      begin
        FSorted := Sorted;

        if FSorted then
        begin
          List := TStringList.Create;
          try
            LocalIniFile := TIniFile.create(FIniFile);

            try
              List.Clear;

              ReadIniSection(List, LocalIniFile, bChanged);

              if FLastItemIndex>0 then
                sLastFile := List.Strings[FLastItemIndex-1]
              else
               sLastFile := '';

              List.Sort;

              FLastItemIndex := List.IndexOf(sLastFile)+1;

              WriteIniSection(List, LocalIniFile);

              InternalUpdateParentMenu(List);
            finally
              LocalIniFile.Free;
            end;
          finally
            List.Free;
          end;
        end
        else
          UpdateParentMenu;
      end;
   end;
end;

procedure THistoryFiles.SetPosition(const Value: Integer);
begin
  if AsSigned(FParentMenu) then
    begin
      if Value>FParentMenu.Count then
        MessageDlg(MsgPositionOutOfRange, mtError, [mbOk], 0)
      else
        FPosition:=Value;
    end
  else
    FPosition:=Value;
end;

procedure THistoryFiles.SetItemBitmap(const b: TBitmap);
begin
  if not b.Empty then
    FItemBitmap.Assign(b);
end;

procedure THistoryFiles.SetItemSelectedBitmap(const b: TBitmap);
begin
  if not b.Empty then
    FItemSelectedBitmap.Assign(b);
end;

procedure THistoryFiles.SetParentMenu(const Value: TMenuItem);
begin
  if AsSigned(FParentMenu) then
    ClearMenu(FParentMenu);

  FParentMenu:=Value;

  if AsSigned(FParentMenu) then
  begin
    FOriginalMainMenuItems:=FParentMenu.Count;

    if (csDesigning in ComponentState) and not(csLoading in ComponentState) then
      begin
        if (FPosition>FParentMenu.Count) or (FPosition=0) then
          FPosition:=FParentMenu.Count
      end
    else
      if FPosition>FParentMenu.Count then
        FPosition:=FParentMenu.Count;
  end;
end;

function THistoryFiles.GetItemValue(const Index : integer): string;
begin
  if (Index<0) or (Index>FItems.Count-1) then
    begin
      MessageDlg(MsgIndexOutOfRange, mtError, [mbOk], 0);
      result := '';
    end
  else
    result := FItems.Strings[Index];
end;

procedure THistoryFiles.ClearLastItem;
begin
  FLastItemIndex := 0;
end;

procedure THistoryFiles.DeleteItem(const Index : integer);
var
  List : TStringList;
  bChanged : boolean;
  LocalIniFile : TIniFile;
  sLastFile : string;
begin
bChanged := false;

if Index<0 then
  MessageDlg(MsgIndexOutOfRange, mtError, [mbOk], 0)
else
  begin
    LocalIniFile := TIniFile.create(FIniFile);
    try
      List := TStringList.Create;
      try
        ReadIniSection(List, LocalIniFile, bChanged);

        if Index>List.Count-1 then
          MessageDlg(MsgIndexOutOfRange, mtError, [mbOk], 0)
        else
          begin
            if FLastItemIndex>0 then
              sLastFile := List.Strings[FLastItemIndex-1]
            else
              sLastFile := '';

            List.Delete(Index);

            FLastItemIndex := List.IndexOf(sLastFile)+1;

            WriteIniSection(List, LocalIniFile);

            InternalUpdateParentMenu(List);
          end;
      finally
        List.Free;
      end;
    finally
      LocalIniFile.Free;
    end;
  end;
end;

function THistoryFiles.GetLastItemIndex: integer;
begin
  result := FLastItemIndex-1;
end;

procedure THistoryFiles.SetLastItemIndex(const Index: integer);
begin
    FLastItemIndex := Index+1;
    LastItemIndex_WriteIni;
end;

procedure THistoryFiles.ReadIniSection(var List : TStringList; LocalIniFile : TIniFile; var bChanged : boolean);
var
  B : string;
  n : integer;
  sLastFile : string;
begin
  bChanged := false;
  n := 1;
  B := LocalIniFile.ReadString(FIniKey, inttostr(n), 'empty');

  FLastItemIndex := LocalIniFile.ReadInteger(FIniKey, 'LastItemIndex', 0);
  sLastFile := LocalIniFile.ReadString(FIniKey, inttostr(FLastItemIndex), '');

  while B<>'empty' do
  begin
    if List.IndexOf(B)<0 then
    begin
        {$IFDEF FPC} //Lazarus
          if not(FFileMustExist and not FileExistsUTF8(B)) then
        {$ELSE}
          if not(FFileMustExist and not FileExists(B)) then
        {$ENDIF}
        List.Add(B)
      else
        bChanged := true;
    end;

    Inc(n);
    B := LocalIniFile.ReadString(FIniKey, inttostr(n), 'empty');
  end;

  FLastItemIndex := List.IndexOf(sLastFile)+1;
end;

procedure THistoryFiles.LastItemIndex_WriteIni;
var
  LocalIniFile : TIniFile;
begin
    LocalIniFile := TIniFile.create(FIniFile);
    try
      LocalIniFile.WriteInteger(FIniKey, 'LastItemIndex', FLastItemIndex);
    finally
      LocalIniFile.Free;
    end;
end;

procedure THistoryFiles.WriteIniSection(const List : TStringList; LocalIniFile : TIniFile);
var
  n : integer;
  iListCount : integer;
begin

  if not(FSorted) and (List.Count > FMaxItems) then
    iListCount := FMaxItems
  else
    iListCount := List.Count;

  if FLastItemIndex > iListCount then
    FLastItemIndex := 0;

  LocalIniFile.EraseSection(FIniKey);

  for n:=0 to iListCount-1 do
    LocalIniFile.WriteString(FIniKey, inttostr(n+1), List.Strings[n]);

  LocalIniFile.WriteInteger(FIniKey, 'LastItemIndex', FLastItemIndex);
end;

procedure THistoryFiles.OnMainMenuClickHistoryItem(Sender:TObject);
var
  thefile : string;
begin
  thefile:='';
  If AsSigned(FOnHistoryItemClick) Then
  begin
   thefile := FItems.Strings[TMenuItem(sender).tag-1];
   if thefile<>'' then
     FLastItemIndex := TMenuItem(sender).tag;

     LastItemIndex_WriteIni;

     FOnHistoryItemClick(Self, TMenuItem(sender), thefile);

     UpdateParentMenu;
  end;
end;

procedure THistoryFiles.ClearMenu(MainMenu: TMenuItem);
var i : integer;
begin
  for i:= 1 to FNumberOfItems do
    MainMenu.items[FPosition].destroy;

  FNumberOfItems:=0;
  FCount:=0;
  FItems.Clear;
end;

procedure THistoryFiles.UpdateList(thefile: string);
 var
  A: string;
  LocalIniFile : TIniFile;
  List : TStringList;
  bChanged : boolean;
begin

List := TStringList.Create;
try
  bChanged := false;
  LocalIniFile := TIniFile.create(FIniFile);

  try
    List.Clear;

    A := thefile;

    if ExtractFilePath(A)='' then
      A:=FLocalPath+A;

    List.Add(A);

    ReadIniSection(List, LocalIniFile, bChanged);
    FLastItemIndex := 1;

    if FSorted then
    begin
      List.Sort;

      FLastItemIndex := List.IndexOf(A)+1;
    end;

    WriteIniSection(List, LocalIniFile);

    InternalUpdateParentMenu(List);
  finally
    LocalIniFile.Free;
  end;
finally
  List.Free;
end;
end;

procedure THistoryFiles.UpdateParentMenu;
var List : TStringList;
begin
  List := TStringList.Create;
  try
    InternalUpdateParentMenu(List);
  finally
    List.Free;
  end;
end;

procedure THistoryFiles.InternalUpdateParentMenu(const CurrentList : TStringList);
var
  LocalIniFile : TIniFile;
  NewItem: TMenuItem;
  A: string;
  n: integer;
  bSepTop : boolean;
  s : string;
  List : TStringList;
  bChanged : boolean;
  iListCount : integer;
begin

if AsSigned(FParentMenu) then
begin
  bSepTop:=False;
  bChanged := false;

  List := TStringList.Create;

  try
    List.Clear;
    ClearMenu(FParentMenu);

    if CurrentList.Count = 0 then
      begin
        LocalIniFile := TIniFile.create(FIniFile);
        try
          ReadIniSection(List, LocalIniFile, bChanged);

          if bChanged then
            WriteIniSection(List, LocalIniFile);
        finally
          LocalIniFile.Free;
        end;
      end
    else
      begin
        for n := 0 to CurrentList.Count-1 do
          List.Add(CurrentList.Strings[n]);
      end;

    if not(FSorted) and (List.Count > FMaxItems) then
      iListCount := FMaxItems
    else
      iListCount := List.Count;

    if FLastItemIndex > iListCount then
      FLastItemIndex := 0;

    for n := 0 to iListCount-1 do
    begin
      A := List.Strings[n];

      if A<>'empty' then
      begin
        if (FSeparator in [sepTop,sepBoth]) and not(bSepTop) then
        begin
          bSepTop:=True;
          NewItem := TMenuItem.Create(FParentMenu);
          NewItem.Caption := '-';
          FParentMenu.insert(FPosition+FNumberOfItems,NewItem);
          Inc(FNumberOfItems);
        end;

        NewItem := TMenuItem.Create(FParentMenu);

        if FShowFullPath then
          begin
            if Upper(ExtractFilePath(A))=Upper(FLocalPath) then
              s := ExtractFileName(A)
            else
              s:=A;
          end
        else
          s:=ExtractFileName(A);

        if FShowNumber then
          NewItem.Caption := '&'+ inttostr(n+1) + ' ' + s
        else
          NewItem.Caption := s;

        if FCheckLastItem and (n = FLastItemIndex-1) then
          begin
            if not FItemSelectedBitmap.Empty then
              NewItem.Bitmap := FItemSelectedBitmap
            else
              NewItem.Checked := true;
          end
        else
          begin
            if not FItemBitmap.Empty then
              NewItem.Bitmap := FItemBitmap;
          end;

        {$IFDEF FPC}
           NewItem.onclick :=  OnMainMenuClickHistoryItem; //Lazarus
        {$ELSE}
           NewItem.onclick :=  OnMainMenuClickHistoryItem;
        {$ENDIF}

        NewItem.tag := n+1;

        FItems.Add(A);
        FParentMenu.Insert(FPosition+FNumberOfItems,NewItem);

        if AsSigned(FOnHistoryCreateItem) then
          FOnHistoryCreateItem(Self,NewItem,A);

        Inc(FNumberOfItems);
        Inc(FCount);
      end;
    end;

    if (FSeparator in [sepBottom,sepBoth]) and (FNumberOfItems>0) then
    begin
      NewItem := TMenuItem.Create(FParentMenu);
      NewItem.Caption := '-';
      FParentMenu.insert(FPosition+FNumberOfItems,NewItem);
      Inc(FNumberOfItems);
    end;

  finally
    List.Free;
  end;
end
  else
    MessageDlg(MsgParentMenuNotAssigned, mtError, [mbOk], 0);
end;

{$IFDEF FPC} //Lazarus
  initialization
    {$i HistoryLazarus.lrs}
{$ENDIF}
end.
