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
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import {
  ProductDisapproval,
  ProductDisapprovalsService
} from '../product-disapprovals.service';

@Component({
  selector: 'mcrb-product-disapproval-list',
  templateUrl: './product-disapproval-list.component.html',
  styleUrls: ['./product-disapproval-list.component.scss']
})

export class ProductDisapprovalListComponent
  implements OnInit, OnDestroy {

  constructor(
    private pdService: ProductDisapprovalsService) {
  }

  sub!: Subscription;
  errorMessage: any;
  pageTitle: string = 'Product Disapprovals';
  filteredPDisapprovals: ProductDisapproval[] = [];
  displayedColumns: string[] = [
    'severity',
    'name',
    'productCount',
    'cta'];

  private _listFilter: string = '';

  get listFilter(): string {
    return this._listFilter;
  }

  set listFilter(value: string) {
    this._listFilter = value;
    this.filteredPDisapprovals = this.performFilter(value);
  }

  get pDisapprovalsCount(): number {
    // todo: refactor when we have actual products
    return this.filteredPDisapprovals
      .reduce((a, b) => a + b.productCount, 0);
  }


  performFilter(filterBy: string): ProductDisapproval[] {
    if (!filterBy) return this.filteredPDisapprovals;
    filterBy = filterBy.toLocaleLowerCase();
    this.pdService
      .getProductDisapprovals()
      .subscribe({
        next: pds => this.filteredPDisapprovals
          = pds.filter((pd: ProductDisapproval) =>
            pd.name
              .toLocaleLowerCase()
              .includes(filterBy)),
        error: err => this.errorMessage = err
      })

    return this.filteredPDisapprovals;
  }

  ngOnInit(): void {
    this.sub = this.pdService
      .getProductDisapprovals()
      .subscribe({
        next: pds => this.filteredPDisapprovals = pds,
        error: err => this.errorMessage = err
      });
    this.listFilter = '';
  }

  ngOnDestroy(): void {
    this.sub.unsubscribe();
  }
}