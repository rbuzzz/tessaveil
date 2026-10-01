#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use slint::{Model, ModelRc, ModelTracker, SharedString, StandardListViewItem, TableColumn};
use std::rc::Rc;
slint::include_modules!();

struct Cells(usize);
impl Model for Cells {
    type Data = StandardListViewItem;
    fn row_count(&self) -> usize {
        36
    }
    fn row_data(&self, column: usize) -> Option<Self::Data> {
        (column < 36).then(|| {
            StandardListViewItem::from(format!("TEST-R{:05}-C{:02}", self.0, column).as_str())
        })
    }
    fn model_tracker(&self) -> &dyn ModelTracker {
        &()
    }
}
struct Rows;
impl Model for Rows {
    type Data = ModelRc<StandardListViewItem>;
    fn row_count(&self) -> usize {
        10000
    }
    fn row_data(&self, row: usize) -> Option<Self::Data> {
        (row < 10000).then(|| ModelRc::from(Rc::new(Cells(row))))
    }
    fn model_tracker(&self) -> &dyn ModelTracker {
        &()
    }
}
fn main() -> Result<(), slint::PlatformError> {
    let app = Probe::new()?;
    app.set_rows(ModelRc::from(Rc::new(Rows)));
    app.set_columns(ModelRc::from(Rc::new(slint::VecModel::from(
        (0..36)
            .map(|c| {
                let mut column = TableColumn::default();
                column.title = SharedString::from(if c < 10 {
                    c.to_string()
                } else {
                    ((b'A' + c - 10) as char).to_string()
                });
                column.width = 172.0;
                column
            })
            .collect::<Vec<_>>(),
    ))));
    app.on_invoke_core(|| probe_core::probe_core_version() as i32);
    app.run()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn lazy_rows_cover_exact_bounds() {
        assert_eq!(Rows.row_count(), 10000);
        assert!(Rows.row_data(10000).is_none());
        let last = Rows.row_data(9999).unwrap();
        assert_eq!(last.row_count(), 36);
        assert_eq!(last.row_data(35).unwrap().text, "TEST-R09999-C35");
        assert!(last.row_data(36).is_none());
    }
}
