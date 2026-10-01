using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using Avalonia;
using Avalonia.Automation;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Controls.Templates;
using Avalonia.Layout;
using Avalonia.Media;
using Avalonia.Markup.Xaml.Styling;
using Avalonia.Markup.Xaml;
using Avalonia.Styling;
using Avalonia.Themes.Fluent;

internal static class Program
{
    [STAThread] public static void Main(string[] args) => AppBuilder.Configure<ProbeApp>().UsePlatformDetect().StartWithClassicDesktopLifetime(args);
    [DllImport("probe_core", EntryPoint = "probe_core_version")] internal static extern uint CoreVersion();
}
public class ProbeApp : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }
    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop) desktop.MainWindow = new ProbeWindow();
        base.OnFrameworkInitializationCompleted();
    }
}
sealed record SyntheticRow(int Number);
sealed class Rows : IReadOnlyList<SyntheticRow>
{
    public int Count => 10000;
    public SyntheticRow this[int index] => index is >= 0 and < 10000 ? new(index) : throw new ArgumentOutOfRangeException(nameof(index));
    public IEnumerator<SyntheticRow> GetEnumerator() { for (int i = 0; i < Count; i++) yield return this[i]; }
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
sealed class ProbeWindow : Window
{
    public ProbeWindow()
    {
        Title = "Tessaveil synthetic Avalonia probe"; Width = 1280; Height = 720;
        var input = new TextBox { PasswordChar = '●', Text = "TEST-INPUT-42!", Width = 250 };
        AutomationProperties.SetName(input, "Test input");
        var result = new TextBlock { Text = "Core: 0" };
        var invoke = new Button { Content = "Invoke core" };
        invoke.Click += (_, _) => { result.Text = $"Core: {Program.CoreVersion()}"; input.Text = ""; };
        var theme = new Button { Content = "Theme" };
        theme.Click += (_, _) => { bool dark = RequestedThemeVariant != ThemeVariant.Dark; RequestedThemeVariant = dark ? ThemeVariant.Dark : ThemeVariant.Light; Background = Brush.Parse(dark ? "#171717" : "#FFFFFF"); Foreground = Brush.Parse(dark ? "#FFFFFF" : "#171717"); };
        var bar = new StackPanel { Orientation = Orientation.Horizontal, Spacing = 12, Children = { new TextBlock { Text = "Test input" }, input, invoke, theme, result } };
        var table = new DataGrid { ItemsSource = new Rows(), IsReadOnly = true, AutoGenerateColumns = false, HeadersVisibility = DataGridHeadersVisibility.All };
        for (int i = 0; i < 36; i++)
        {
            int column = i;
            table.Columns.Add(new DataGridTemplateColumn {
                Header = i < 10 ? i.ToString() : ((char)('A' + i - 10)).ToString(), Width = new DataGridLength(172),
                CellTemplate = new FuncDataTemplate<SyntheticRow>((row, _) => new TextBlock { Text = $"TEST-R{row!.Number:00000}-C{column:00}" })
            });
        }
        var layout = new DockPanel { Margin = new Thickness(12) };
        DockPanel.SetDock(bar, Dock.Top); layout.Children.Add(bar); layout.Children.Add(table); Content = layout;
    }
}
