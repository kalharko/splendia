import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { AppService } from 'src/app/shared/services/app.service';

@Component({
  selector: 'app-reject-token',
  templateUrl: './reject-token.component.html',
  styleUrls: ['./reject-token.component.scss']
})
export class RejectTokenComponent implements OnInit {

  tokensToReject: number[] = [0, 0, 0, 0, 0, 0];
  constructor(  private appService: AppService, 
    public dialogRef: MatDialogRef<RejectTokenComponent>) { }

  ngOnInit(): void {
  }

  rejectTokenConfirmation():void{
    this.appService.rejectToken(this.tokensToReject);
  
  }

}
