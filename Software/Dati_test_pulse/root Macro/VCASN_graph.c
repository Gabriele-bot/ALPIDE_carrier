#include "TCanvas.h"
#include "TROOT.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TArrow.h"


void Draw_graph_VCASN()
{
	TGraphErrors graph("Soglia_VCASN.txt");
	graph.SetTitle("V_{CASN} dependency;V_{CASN} [mV];Threshold [e^{-}]");

	graph.SetMarkerStyle(6);
	graph.SetMarkerColor(kBlue);
	graph.SetLineColor(kBlue);

	auto mycanvas = new TCanvas();
	mycanvas->SetGrid();

	graph.DrawClone("APE");
	TF1 f("V_{CASN} dependency","[0]*x+[1]",0,510);
	f.SetLineColor(kRed);
	f.SetLineStyle(1);
	f.SetParameters(0.7,500);
	f.SetParNames("a","b");

	auto fitResPtr=graph.Fit(&f);
	
	f.DrawClone("Same");
	graph.DrawClone("APE");

	TLegend leg(.1,.7,.3,.9,"V_{CASN} dependency");
	leg.SetFillColor(0);
	graph.SetFillColor(0);
	leg.AddEntry(&graph,"Exp. Points");
	leg.AddEntry(&f,"Linear fit");
	leg.DrawClone("Same");


}

int main(){
	Draw_graph_VCASN();
	}
