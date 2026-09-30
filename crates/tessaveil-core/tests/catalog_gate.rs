use tessaveil_core::catalog;

#[test]
fn only_projected_approved_pairs_can_be_selected() {
    let profiles = catalog::profiles().unwrap();
    let selected: Vec<_> = profiles
        .iter()
        .filter(|p| p.selectable())
        .map(|p| (p.id(), p.mode()))
        .collect();
    assert_eq!(
        selected,
        vec![
            ("mytonwallet-native", "ton-native-generated"),
            ("tonhub", "ton-native-generated"),
            ("tonkeeper-classic", "ton-native-generated"),
        ]
    );
    assert!(profiles.len() > 100);
    for p in profiles {
        if !p.selectable() {
            assert!(!p.reason().is_empty());
            assert!(catalog::select(p.id(), p.mode()).is_err());
        }
    }
    assert!(catalog::select("tonhub", "wrong-mode").is_err());
}
