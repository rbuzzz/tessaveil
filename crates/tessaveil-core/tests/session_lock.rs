use std::time::{Duration, Instant};
use tessaveil_core::session::{Inactivity, Session};
#[test]
fn timeout_choices_and_stale_tokens_are_enforced() {
    for n in [1, 5, 15, 30] {
        assert_eq!(
            Inactivity::from_minutes(n).unwrap().duration(),
            Duration::from_secs(n as u64 * 60)
        );
    }
    for n in [0, 2, 60, 255] {
        assert!(Inactivity::from_minutes(n).is_err());
    }
    assert_eq!(Inactivity::default().duration(), Duration::from_secs(300));
    let now = Instant::now();
    let mut s = Session::new(Inactivity::default(), now);
    let old = s.token();
    assert!(!s.is_expired(old, now + Duration::from_secs(299)));
    let current = s.activity(now + Duration::from_secs(100));
    assert!(!s.is_expired(old, now + Duration::from_secs(900)));
    assert!(!s.is_expired(current, now + Duration::from_secs(399)));
    assert!(s.is_expired(current, now + Duration::from_secs(400)));
    let other = Session::new(Inactivity::default(), now + Duration::from_secs(100));
    assert!(!other.is_expired(current, now + Duration::from_secs(900)));
}
#[test]
fn changing_timeout_invalidates_previous_timer() {
    let now = Instant::now();
    let mut s = Session::new(Inactivity::default(), now);
    let old = s.token();
    let new = s.set_inactivity(Inactivity::OneMinute, now);
    assert!(!s.is_expired(old, now + Duration::from_secs(300)));
    assert!(s.is_expired(new, now + Duration::from_secs(60)));
}
