/*
Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { catchError, Observable, tap, throwError } from "rxjs";
import { AppConfigService } from "../app-config-service";

export interface ProductDisapprovalCta {
  doc: string;
  action: string;
}

export interface ProductDisapproval {
  name: string;
  code: string;
  severity: string;
  cta?: ProductDisapprovalCta;
  productCount: number
}

@Injectable({
  providedIn: 'root'
})
export class ProductDisapprovalsService {
  baseUrl: string;
  private productDisapprovalsUrl: string = '';
  
  constructor(private http: HttpClient, 
    environment: AppConfigService){
      this.baseUrl = window.location.href.indexOf('localhost') > -1 
        ? 'http://localhost:8080'
        : environment.appConfig.webapiUrl;
      this.productDisapprovalsUrl = this.baseUrl + '/product-disapprovals';
    }

  getProductDisapprovals(): Observable<ProductDisapproval[]> {
    return this.http.get<ProductDisapproval[]>(this.productDisapprovalsUrl)
      .pipe(
        tap(data => console.log('Pds: ', JSON.stringify(data))),
        catchError(this.handleError)
      );
  }
  
  private handleError(err: HttpErrorResponse){
    let errorMessage = (err.error instanceof ErrorEvent)
      ? `An error occurred: ${err.error.message}`
      : `Server returned code: ${err.status}, error is: ${err.message}`;
    return throwError(() => errorMessage)
  }

  get mapCodetoStoreBuilderCta()
    : { [key: string]: ProductDisapprovalCta } {
    return {
      "TBX-00": {
        doc: "http://SB-00-documentation",
        action: "http://SB-00-action"
      },
      "TBX-01": {
        doc: "http://SB-00-documentation",
        action: "http://SB-00-action"
      }
    }
  }

  get defaultMapCodetoCta()
    : { [key: string]: ProductDisapprovalCta } {
    return {
      "TBX-00": {
        doc: "http://google.com?s=SB-00-documentation",
        action: "http://google.com?s=SB-00-action"
      },
      "TBX-01": {
        doc: "http://google.com?s=SB-0001-documentation",
        action: "http://google.com?s=SB-001-action"
      },
      "TBX-02": {
        doc: "https://support.google.com/merchants/answer/160050?hl=en",
        action: "http://google.com?s=SB-02-action"
      },
      "TBX-03": {
        doc: "https://support.google.com/merchants/answer/160050?hl=en",
        action: "http://google.com?s=SB-03-action"
      }
    }
  }



}

