import React from "react";
import { useMsal } from "@azure/msal-react";
import { Card, CardHeader, CardTitle, CardContent } from "../components/ui/card";

const Dashboard: React.FC = () => {
  const { accounts } = useMsal();
  const email = accounts[0]?.username || "User";

  return (
    <div className="container mx-auto mt-8">
      <Card>
        <CardHeader>
          <CardTitle>Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg">Welcome, {email}!</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;